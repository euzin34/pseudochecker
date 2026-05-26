const sourceEl = document.getElementById("source");
// Initialize CodeMirror editor from the textarea
let editor = null;
if (typeof CodeMirror !== "undefined") {
  editor = CodeMirror.fromTextArea(sourceEl, {
    lineNumbers: true,
    mode: "pseudocode",
    theme: "material-darker",
    indentUnit: 4,
    tabSize: 4,
    autofocus: true,
    viewportMargin: Infinity,
  });
} else {
  console.warn("CodeMirror not loaded; falling back to textarea editor.");
}

function getSourceValue() { return editor ? editor.getValue() : sourceEl.value; }
function setSourceValue(v) { if (editor) editor.setValue(v); else sourceEl.value = v; }
function focusSource() { if (editor) editor.focus(); else sourceEl.focus(); }

const issueListEl = document.getElementById("issue-list");
const noIssuesEl = document.getElementById("no-issues");
const statusBanner = document.getElementById("status-banner");
const pythonPreviewEl = document.getElementById("python-preview");
const exampleSelect = document.getElementById("example-select");
const btnCheck = document.getElementById("btn-check");
const btnClear = document.getElementById("btn-clear");

async function loadExamples() {
  try {
    const res = await fetch("/api/examples");
    const data = await res.json();
    for (const name of data.examples || []) {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name.replace(/_/g, " ");
      exampleSelect.appendChild(opt);
    }
  } catch (e) {
    console.warn("Could not load examples", e);
  }
}

exampleSelect.addEventListener("change", async () => {
  const name = exampleSelect.value;
  if (!name) return;
  const res = await fetch(`/api/examples/${name}`);
  if (!res.ok) return;
  const data = await res.json();
  setSourceValue(data.source);
  clearResults();
});

btnClear.addEventListener("click", () => {
  setSourceValue("");
  exampleSelect.value = "";
  clearResults();
});

btnCheck.addEventListener("click", runCheck);
if (editor) {
  editor.setOption("extraKeys", {"Ctrl-Enter": runCheck});
} else {
  sourceEl.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key === "Enter") runCheck();
  });
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
  });
});

function clearResults() {
  issueListEl.innerHTML = "";
  noIssuesEl.classList.add("hidden");
  statusBanner.classList.add("hidden");
  pythonPreviewEl.textContent = "Run Check to generate a Python preview.";
  if (editor) {
    // clear any previous highlighted line
    if (typeof editor._currentLine !== 'undefined' && editor._currentLine !== null) {
      editor.removeLineClass(editor._currentLine, "background", "line-highlight");
      editor._currentLine = null;
    }
  } else {
    sourceEl.classList.remove("line-highlight");
  }
}

function scrollToLine(line) {
  if (editor) {
    const doc = editor.getDoc();
    const last = doc.lastLine();
    const target = Math.max(0, Math.min(line - 1, last));
    editor.focus();
    doc.setCursor({line: target, ch: 0});
    editor.scrollIntoView({line: target, ch: 0}, 100);
    if (typeof editor._currentLine !== 'undefined' && editor._currentLine !== null) {
      editor.removeLineClass(editor._currentLine, "background", "line-highlight");
    }
    editor.addLineClass(target, "background", "line-highlight");
    editor._currentLine = target;
  } else {
    const lines = sourceEl.value.split("\n");
    let pos = 0;
    for (let i = 0; i < line - 1 && i < lines.length; i++) {
      pos += lines[i].length + 1;
    }
    sourceEl.focus();
    sourceEl.setSelectionRange(pos, pos + (lines[line - 1]?.length || 0));
    sourceEl.scrollTop = Math.max(0, (line - 1) * 18 - 60);
    sourceEl.classList.add("line-highlight");
  }
}

function renderIssues(errors, warnings) {
  issueListEl.innerHTML = "";
  const all = [...errors, ...warnings];
  if (all.length === 0) {
    noIssuesEl.classList.remove("hidden");
    return;
  }
  noIssuesEl.classList.add("hidden");
  for (const item of all) {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="severity ${item.severity}">${item.type}</div>
      <div class="location">Line ${item.line}, column ${item.column}</div>
      <div>${escapeHtml(item.message)}</div>
      ${item.suggestion ? `<div class="muted">Suggestion: ${escapeHtml(item.suggestion)}</div>` : ""}
    `;
    if (item.line > 1) {
      li.addEventListener("click", () => scrollToLine(item.line));
    }
    issueListEl.appendChild(li);
  }
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

async function runCheck() {
  clearResults();
  btnCheck.disabled = true;
  btnCheck.textContent = "Checking…";

  try {
    const res = await fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: getSourceValue(), include_python_preview: true }),
    });
    const data = await res.json();

    statusBanner.classList.remove("hidden", "success", "error", "warning");
    if (data.ok && (!data.warnings || data.warnings.length === 0)) {
      statusBanner.classList.add("success");
      statusBanner.textContent = data.message || "Valid pseudocode.";
    } else if (data.ok) {
      statusBanner.classList.add("warning");
      statusBanner.textContent = data.message || "Valid with warnings.";
    } else {
      statusBanner.classList.add("error");
      statusBanner.textContent = data.message || "Validation failed.";
    }

    if (data.stats) {
      const s = data.stats;
      const extra = ` · ${s.token_count || 0} tokens · ${s.statement_count || 0} statements`;
      statusBanner.textContent += extra;
    }

    renderIssues(data.errors || [], data.warnings || []);

    if (data.python_preview) {
      pythonPreviewEl.textContent = data.python_preview;
      pythonPreviewEl.classList.remove("muted");
    } else {
      pythonPreviewEl.textContent = "No Python preview (fix errors first).";
      pythonPreviewEl.classList.add("muted");
    }
  } catch (e) {
    statusBanner.classList.remove("hidden");
    statusBanner.classList.add("error");
    statusBanner.textContent = "Network error: " + e.message;
  } finally {
    btnCheck.disabled = false;
    btnCheck.textContent = "Check";
  }
}

function debounce(fn, wait) {
  let t = null;
  return function(...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), wait);
  };
}

// Live check wiring
const liveCheckEl = document.getElementById('live-check');
const debouncedRun = debounce(() => {
  if (getSourceValue().trim()) runCheck();
}, 700);

if (editor) {
  editor.on('change', () => {
    if (liveCheckEl && liveCheckEl.checked) debouncedRun();
  });
} else {
  sourceEl.addEventListener('input', () => {
    if (liveCheckEl && liveCheckEl.checked) debouncedRun();
  });
}

loadExamples();
