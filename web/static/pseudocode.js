(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["codemirror"], mod);
  else // Plain browser env
    mod(window.CodeMirror);
})(function(CodeMirror) {
  "use strict";

  var keywords = {
    "DECLARE": true,
    "CONSTANT": true,
    "IF": true,
    "THEN": true,
    "ELSE": true,
    "ELSEIF": true,
    "ENDIF": true,
    "FOR": true,
    "TO": true,
    "STEP": true,
    "NEXT": true,
    "WHILE": true,
    "REPEAT": true,
    "UNTIL": true,
    "CASE": true,
    "OF": true,
    "PROCEDURE": true,
    "FUNCTION": true,
    "RETURN": true,
    "OUTPUT": true,
    "INPUT": true,
    "ARRAY": true,
    "SELECT": true,
    "WHEN": true,
    "DEFAULT": true
  };

  var types = {
    "INTEGER": true,
    "REAL": true,
    "STRING": true,
    "CHAR": true,
    "BOOLEAN": true
  };

  var builtins = {
    "TRUE": true,
    "FALSE": true,
    "AND": true,
    "OR": true,
    "NOT": true
  };

  CodeMirror.defineMode("pseudocode", function(config, parserConfig) {
    return {
      startState: function() { return {}; },
      token: function(stream, state) {
        if (stream.eatSpace()) return null;

        // Line comment //
        if (stream.match("//")) {
          stream.skipToEnd();
          return "comment";
        }

        // Strings
        if (stream.match(/^"(?:[^"\\]|\\.)*"/) || stream.match(/^'(?:[^'\\]|\\.)*'/)) {
          return "string";
        }

        // Numbers
        if (stream.match(/^[0-9]+(\.[0-9]+)?/)) return "number";

        // Identifiers / keywords
        if (stream.match(/^[A-Za-z_][A-Za-z0-9_]*/)) {
          var cur = stream.current().toUpperCase();
          if (keywords[cur]) return "keyword";
          if (types[cur]) return "variable-2";
          if (builtins[cur]) return "atom";
          return "variable";
        }

        // Operators
        if (stream.match(/^[+\-*/=<>!:]+/)) return "operator";

        // Punctuation
        if (stream.match(/^[\[\]\(\),]/)) return null;

        // Move forward
        stream.next();
        return null;
      }
    };
  });

  CodeMirror.defineMIME("text/x-pseudocode", "pseudocode");
});
