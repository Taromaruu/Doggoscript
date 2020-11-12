CodeMirror.defineSimpleMode("doggoscript", {
    start: [
      {regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string"},
      {regex: /(?:var|if|elif|else|for|step|while|fun|and|or|not|to|then|end|return|continue|break)\b/,
       token: "keyword"},
      {regex: /(?:print|print_ret|input|input_int|clear|is_number|is_string|is_list|is_function|append|pop|extend|run|sqrt|len|lower|random|print_end|input_prompt)\b/, token: "builtin"},
      {regex: /true|false|null|pi/, token: "atom"},
      {regex: /0x[\d]+|[-+]?(?:\d+\.?\d*)(?:e[-+]?\d+)?/i,
       token: "number"},
      {regex: /\#.*/, token: "comment"},
      {regex: /[-+\/*=<>!]+/, token: "operator"},
      {regex: /[a-z|A-Z$][\w$]*/, token: "variable"},
    ],
    meta: {
      dontIndentStates: ["comment"],
      lineComment: "#"
    }
  });
  