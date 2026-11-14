/* Arduino C++ (a teaching subset) -> JavaScript translator for the Voltaic microcontroller.
   It is NOT a compiler: the output is JavaScript that the simulator's runtime executes (see sim.js, class Mcu).

   Supported:  void setup() / void loop(), your own functions (they may call delay()), int/long/short/unsigned/byte/
               bool/char/float/double/String variables, const, #define NAME value, one-dimensional arrays,
               if/else, for, while, do-while, switch, ?:, casts (int)/(float), the pin/time/Serial functions of Arduino.
   C++ behaviour that is kept: integer division and integer variables truncate, bool prints as 0/1.
   NOT supported: classes/structs/enum/typedef/templates, pointers and references, other libraries, static locals,
               2-D arrays, interrupts, RTOS. These give an error that names the construct and the line.

   Used in the browser (global functions) and in Node tests (module.exports). */

const CPP_INT = new Set(['int', 'long', 'short', 'unsigned', 'signed', 'bool', 'boolean', 'byte', 'char', 'size_t', 'word',
  'uint8_t', 'int8_t', 'uint16_t', 'int16_t', 'uint32_t', 'int32_t', 'uint64_t', 'int64_t']);
const CPP_FLOAT = new Set(['float', 'double']);
const CPP_QUAL = new Set(['const', 'static', 'volatile', 'register', 'inline', 'constexpr']);
const CPP_TYPE = new Set([...CPP_INT, ...CPP_FLOAT, 'void', 'String', 'auto']);
const CPP_BAD = new Set(['class', 'struct', 'enum', 'union', 'typedef', 'template', 'namespace', 'using', 'new', 'delete',
  'try', 'catch', 'throw', 'goto', 'operator', 'friend', 'virtual', 'public', 'private', 'protected', 'extern', 'sizeof']);
const CPP_KW = new Set(['return', 'case', 'else', 'do', 'if', 'while', 'for', 'switch']);
const CPP_INTCALLS = new Set(['millis', 'micros', 'analogRead', 'digitalRead', 'random', 'map', 'trunc', 'length']);
const CPP_TRANSPARENT = new Set(['abs', 'min', 'max', 'constrain']);   // int if all arguments are int
const CPP_OPS = ['<<=', '>>=', '...', '->', '::', '++', '--', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>'];

function isCpp(src) { return /\bvoid\s+(setup|loop)\s*\(/.test(String(src || '')); }

function cppErr(line, msg) { const e = new Error('line ' + line + ': ' + msg); e.line = line; return e; }

function cppLex(src) {
  const toks = []; let i = 0, line = 1, atStart = true; const n = src.length;
  const push = (t, s, extra) => { toks.push(Object.assign({ t, s, line }, extra || {})); if (t !== 'ws') atStart = false; };
  while (i < n) {
    const c = src[i];
    if (c === '\n') { push('ws', '\n'); line++; i++; atStart = true; continue; }
    if (c === ' ' || c === '\t' || c === '\r') { push('ws', c); i++; continue; }
    if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; continue; }
    if (c === '/' && src[i + 1] === '*') {
      const j = src.indexOf('*/', i + 2), end = j < 0 ? n : j + 2, nl = (src.slice(i, end).match(/\n/g) || []).length;
      push('ws', ' ' + '\n'.repeat(nl)); line += nl; i = end; continue;
    }
    if (c === '#' && atStart) {
      let j = i, text = '';
      while (j < n) { if (src[j] === '\n') { if (text.endsWith('\\')) { text = text.slice(0, -1) + ' '; j++; line++; continue; } break; } text += src[j]; j++; }
      push('pp', text); i = j; continue;
    }
    if (c === '"') {
      let j = i + 1; while (j < n && src[j] !== '"' && src[j] !== '\n') { if (src[j] === '\\') j++; j++; }
      if (src[j] !== '"') throw cppErr(line, 'string is not closed');
      push('str', src.slice(i, j + 1)); i = j + 1; continue;
    }
    if (c === "'") {
      let j = i + 1; while (j < n && src[j] !== "'" && src[j] !== '\n') { if (src[j] === '\\') j++; j++; }
      if (src[j] !== "'") throw cppErr(line, 'character literal is not closed');
      const body = src.slice(i + 1, j); let code;
      if (body[0] === '\\') code = { n: 10, t: 9, r: 13, '0': 0, '\\': 92, "'": 39, '"': 34 }[body[1]] ?? body.charCodeAt(1);
      else code = body.charCodeAt(0);
      push('num', String(code), { f: false }); i = j + 1; continue;
    }
    const re = /0[xX][0-9a-fA-F]+[uUlL]*|0[bB][01]+[uUlL]*|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?[fFuUlL]*/y; re.lastIndex = i;
    const m = (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1] || ''))) ? re.exec(src) : null;
    if (m) {
      const raw = m[0], hex = /^0[xXbB]/.test(raw), clean = raw.replace(/[uUlL]+$/, '').replace(hex ? /$^/ : /[fF]$/, '');
      push('num', clean, { f: !hex && (/[.eE]/.test(clean) || /[fF]$/.test(raw)) }); i += raw.length; continue;
    }
    const id = /[A-Za-z_]\w*/y; id.lastIndex = i; const im = /[A-Za-z_]/.test(c) ? id.exec(src) : null;
    if (im) { push('id', im[0]); i += im[0].length; continue; }
    const op = CPP_OPS.find(o => src.startsWith(o, i));
    if (op) { push('op', op); i += op.length; continue; }
    if ('+-*/%=<>!&|^~?:;,.(){}[]'.includes(c)) { push('op', c); i++; continue; }
    throw cppErr(line, "unexpected character '" + c + "'");
  }
  return toks;
}

function translateCpp(src) {
  const T = cppLex(String(src));
  const N = T.length;
  const sig = i => { while (i < N && T[i].t === 'ws') i++; return i; };
  const sigPrev = i => { i--; while (i >= 0 && T[i].t === 'ws') i--; return i; };
  const match = i => {            // index of the bracket that closes the one at i
    const open = T[i].s; let d = 0;
    for (let j = i; j < N; j++) {
      const s = T[j].t === 'op' ? T[j].s : '';
      if (s === '(' || s === '[' || s === '{') d++;
      else if (s === ')' || s === ']' || s === '}') { d--; if (d === 0) return j; }
    }
    throw cppErr(T[i].line, "'" + open + "' is never closed");
  };
  const isWord = (tk, set) => tk && tk.t === 'id' && set.has(tk.s);

  /* ---- pass 1: user functions and their return kinds */
  const userFns = new Set(), fnKind = {}, globals = new Map(); let locals = null;
  {
    let depth = 0;
    for (let i = 0; i < N; i++) {
      const tk = T[i];
      if (tk.t === 'op' && tk.s === '{') depth++; else if (tk.t === 'op' && tk.s === '}') depth--;
      if (depth === 0 && tk.t === 'id' && !CPP_TYPE.has(tk.s) && !CPP_QUAL.has(tk.s)) {
        const p = sigPrev(i), nx = sig(i + 1);
        if (p >= 0 && isWord(T[p], CPP_TYPE) && T[nx] && T[nx].s === '(') {
          userFns.add(tk.s); let k = p, kind = 'other';
          while (k >= 0 && (isWord(T[k], CPP_TYPE) || isWord(T[k], CPP_QUAL))) { if (CPP_INT.has(T[k].s)) kind = 'int'; else if (CPP_FLOAT.has(T[k].s)) kind = 'float'; k = sigPrev(k); }
          fnKind[tk.s] = kind;
        }
      }
    }
  }
  const kindOf = name => (locals && locals.has(name)) ? locals.get(name) : globals.get(name);
  const declare = (name, kind, depth) => (depth > 0 && locals ? locals : globals).set(name, kind);
  for (const k of ['HIGH', 'LOW', 'INPUT', 'OUTPUT', 'INPUT_PULLUP', 'LED_BUILTIN', 'true', 'false']) globals.set(k, 'int');

  /* ---- is a token range an integer expression? (arrays of tokens {t,s,f}) */
  function isIntRange(A, a, b) {
    const nextSig = i => { i++; while (i < b && A[i].t === 'ws') i++; return i; };
    for (let i = a; i < b; i++) {
      const e = A[i];
      if (e.t === 'ws' || e.t === 'op' || e.t === 'kw' || e.t === 'pp') continue;
      if (e.t === 'mark' || e.t === 'str') return false;
      if (e.t === 'num') { if (e.f) return false; continue; }
      if (e.t === 'id') {
        if (CPP_FLOAT.has(e.s)) return false;
        if (CPP_INT.has(e.s) || CPP_QUAL.has(e.s)) return true;     // a cast to an integer type
        const nx = nextSig(i);
        if (nx < b && A[nx].s === '(' && A[nx].t === 'op') {
          if (CPP_TRANSPARENT.has(e.s) || CPP_KW.has(e.s)) continue;
          if (CPP_INTCALLS.has(e.s) || fnKind[e.s] === 'int') {   // skip the arguments
            let d = 0, j = nx; for (; j < b; j++) { if (A[j].t === 'op' && A[j].s === '(') d++; else if (A[j].t === 'op' && A[j].s === ')') { d--; if (d === 0) break; } }
            i = j; continue;
          }
          return false;
        }
        if (nx < b && A[nx].t === 'op' && A[nx].s === '.') continue;      // namespace-like prefix (Math., Serial.)
        const kd = kindOf(e.s);
        if (kd !== 'int') return false;
        if (nx < b && A[nx].t === 'op' && A[nx].s === '[') { let d = 0, j = nx; for (; j < b; j++) { if (A[j].s === '[') d++; else if (A[j].s === ']') { d--; if (d === 0) break; } } i = j; }
      }
    }
    return true;
  }

  const castAt = i => {            // is the '(' at i the start of a C-style cast like (int) or (unsigned long)?
    if (!(T[i].t === 'op' && T[i].s === '(')) return null;
    const p = sigPrev(i);
    if (p >= 0 && ((T[p].t === 'id' && !CPP_KW.has(T[p].s)) || T[p].s === ')' || T[p].s === ']')) return null;
    let j = sig(i + 1), kind = null, words = 0;
    while (j < N && T[j].t === 'id' && (CPP_TYPE.has(T[j].s) || CPP_QUAL.has(T[j].s))) { if (CPP_FLOAT.has(T[j].s)) kind = 'float'; else if (CPP_INT.has(T[j].s)) kind = kind || 'int'; words++; j = sig(j + 1); }
    if (!words || !kind || !(T[j] && T[j].s === ')')) return null;
    return { kind, end: j };
  };
  function primEnd(i) {            // index just after the primary expression that starts at (or after) i
    i = sig(i); let tk = T[i];
    while (tk && tk.t === 'op' && ['-', '+', '!', '~', '++', '--'].includes(tk.s)) { i = sig(i + 1); tk = T[i]; }
    if (!tk) return i;
    if (tk.t === 'op' && tk.s === '(') { const c = castAt(i); if (c) return primEnd(c.end + 1); i = match(i) + 1; }
    else if (tk.t === 'num' || tk.t === 'str') i++;
    else if (tk.t === 'id') i++;
    else return i + 1;
    for (;;) {
      const j = sig(i), t = T[j];
      if (!t || t.t !== 'op') break;
      if (t.s === '(' || t.s === '[') { i = match(j) + 1; continue; }
      if (t.s === '.') { i = sig(j + 1) + 1; continue; }
      if (t.s === '++' || t.s === '--') { i = j + 1; continue; }
      break;
    }
    return i;
  }
  function rhsEnd(i) {             // end of an initialiser / right-hand side: first top-level ; , or unmatched )
    let d = 0;
    for (let j = i; j < N; j++) {
      const s = T[j].t === 'op' ? T[j].s : '';
      if (s === '(' || s === '[' || s === '{') d++;
      else if (s === ')' || s === ']' || s === '}') { if (d === 0) return j; d--; }
      else if (d === 0 && (s === ';' || s === ',')) return j;
    }
    return N;
  }

  /* ---- output buffer with a few helpers */
  const out = [];
  const emit = (s, t, extra) => out.push(Object.assign({ s, t: t || 'op' }, extra || {}));
  const closeBefore = {}; const braceMap = {}; const guardParen = new Set(); const openAfter = {};
  const addClose = (idx, n) => { closeBefore[idx] = (closeBefore[idx] || 0) + n; };
  const skipNL = (a, b) => { for (let k = a; k < b; k++) if (T[k].t === 'ws') for (const ch of T[k].s) if (ch === '\n') emit('\n', 'ws'); };
  const outPrimStart = e => {      // start index (in out) of the primary expression that ends just before e
    let k = e - 1; while (k >= 0 && out[k].t === 'ws') k--;
    if (k < 0) return e;
    if (out[k].t === 'op' && (out[k].s === ')' || out[k].s === ']')) {
      let d = 0;
      for (; k >= 0; k--) { const s = out[k].t === 'op' ? out[k].s : ''; if (s === ')' || s === ']') d++; else if (s === '(' || s === '[') { d--; if (d === 0) break; } }
      let q = k - 1; while (q >= 0 && out[q].t === 'ws') q--;
      if (q >= 0 && out[q].t === 'id' && !CPP_KW.has(out[q].s)) k = q; else return k;
    } else if (out[k].t === 'id' || out[k].t === 'num' || out[k].t === 'str') { /* simple primary */ }
    else return e;
    for (;;) {                     // member chain: a.b.c
      let q = k - 1; while (q >= 0 && out[q].t === 'ws') q--;
      if (q >= 0 && out[q].t === 'op' && out[q].s === '.') { let r = q - 1; while (r >= 0 && out[r].t === 'ws') r--; if (r >= 0 && out[r].t === 'id') { k = r; continue; } }
      break;
    }
    return k;
  };
  const outChainStart = () => {    // start of the left operand chain  a * b / ... that ends at the end of out
    let j = out.length;
    for (;;) {
      const s = outPrimStart(j);
      let k = s - 1; while (k >= 0 && out[k].t === 'ws') k--;
      if (k >= 0 && out[k].t === 'op' && (out[k].s === '*' || out[k].s === '/' || out[k].s === '%')) { j = k; continue; }
      return s;
    }
  };

  /* ---- pass 2: translate */
  let braceDepth = 0, loopGuards = 0;
  const atStmtStart = i => {
    const p = sigPrev(i);
    if (p < 0) return true;
    if (T[p].t === 'pp') return true;
    const s = T[p].s;
    if (s === ';' || s === '{' || s === '}') return true;
    if (s === '(') { const q = sigPrev(p); return q >= 0 && T[q].s === 'for'; }
    return false;
  };
  const dirTokens = text => cppLex(text).map(x => x.s).join('');

  function declaratorList(i, kind, isConst, line) {      // i = first declarator name; returns index of the terminator
    for (;;) {
      const nameTok = T[i];
      if (!nameTok || nameTok.t !== 'id') throw cppErr(line, 'a variable name was expected here');
      declare(nameTok.s, kind, braceDepth);
      emit(nameTok.s, 'id');
      let j = sig(i + 1);
      if (T[j] && T[j].s === '[') {
        const k = match(j), after = sig(k + 1);
        if (T[after] && T[after].s === '[') throw cppErr(T[j].line, 'two-dimensional arrays are not supported');
        const size = T.slice(j + 1, k).filter(x => x.t !== 'ws').map(x => x.s).join('');
        if (T[after] && T[after].s === '=') {
          const b = sig(after + 1);
          if (!(T[b] && T[b].s === '{')) throw cppErr(T[b] ? T[b].line : line, 'an array needs a { … } initialiser here');
          const bm = match(b); braceMap[b] = '['; braceMap[bm] = ']';
          emit(' = ', 'op'); run(b, bm + 1); i = bm + 1;
        } else {
          emit(' = new Array(' + (size || '0') + ').fill(' + (kind === 'str' ? "''" : '0') + ')', 'op'); i = k + 1;
        }
      } else if (T[j] && T[j].s === '=') {
        const s = sig(j + 1), e = rhsEnd(s);
        emit(' = ', 'op');
        const single = e - s <= 2 && T[s].t === 'num' && !T[s].f;
        const wrap = kind === 'int' && !single;
        if (wrap) { emit('Math', 'id'); emit('.', 'op'); emit('trunc', 'id'); emit('(', 'op'); }
        run(s, e); if (wrap) emit(')', 'op');
        i = e;
      } else {
        emit(kind === 'str' ? " = ''" : ' = 0', 'op'); i = j;
      }
      const t = T[i];
      if (t && t.s === ',') { emit(', ', 'op'); i = sig(i + 1); continue; }
      return i;
    }
  }

  function run(a, b) {
    let i = a;
    while (i < b) {
      if (closeBefore[i]) { for (let k = 0; k < closeBefore[i]; k++) emit(')', 'op'); delete closeBefore[i]; }
      const tk = T[i];
      if (tk.t === 'ws') { emit(tk.s, 'ws'); i++; continue; }
      if (tk.t === 'pp') {
        const text = tk.s.replace(/^#\s*/, '');
        let m;
        if ((m = /^include\s*[<"]([^>"]+)[>"]/.exec(text))) {
          if (m[1] !== 'Arduino.h') throw cppErr(tk.line, "the library '" + m[1] + "' is not available in the simulator (only Arduino.h is)");
        } else if ((m = /^define\s+(\w+)(\(?)\s*(.*)$/.exec(text))) {
          if (m[2]) throw cppErr(tk.line, 'function-like macros are not supported (use a real function)');
          const val = m[3].trim() || '1', vt = cppLex(val).filter(x => x.t !== 'ws');
          globals.set(m[1], vt.length === 1 && vt[0].t === 'num' ? (vt[0].f ? 'float' : 'int') : (vt.length === 1 && vt[0].t === 'id' && kindOf(vt[0].s)) || undefined);
          emit('const ' + m[1] + ' = ' + dirTokens(val) + ';', 'pp');
        } else if (/^pragma\b/.test(text)) { /* ignore */ }
        else throw cppErr(tk.line, "'#" + text.split(/\s/)[0] + "' is not supported (no conditional compilation in the simulator)");
        i++; continue;
      }
      if (tk.t === 'str') { emit(tk.s, 'str'); i++; continue; }
      if (tk.t === 'num') { emit(tk.s, 'num', { f: tk.f }); i++; continue; }
      if (tk.t === 'op') {
        const s = tk.s;
        if (s === '->' || s === '::') throw cppErr(tk.line, "'" + s + "' is not supported (no pointers or namespaces in the simulator)");
        if (s === '{') {
          if (braceMap[i]) { emit(braceMap[i], 'op'); } else { braceDepth++; emit('{', 'op'); }
          i++; continue;
        }
        if (s === '}') {
          if (braceMap[i]) emit(braceMap[i], 'op');
          else { braceDepth--; emit('}', 'op'); if (braceDepth === 0) locals = null; }
          i++; continue;
        }
        if (s === '(') {
          const c = castAt(i);
          if (c) {
            const e = primEnd(c.end + 1);
            if (c.kind === 'int') { emit('Math', 'id'); emit('.', 'op'); emit('trunc', 'id'); emit('(', 'op'); }
            else { emit('(', 'op'); emit('/*f*/', 'mark'); emit('+', 'op'); }
            addClose(e, 1); i = c.end + 1; continue;
          }
          emit('(', 'op'); if (guardParen.has(i)) emit('__g(),', 'kw');
          i++; continue;
        }
        if (s === ';' && openAfter[i]) { emit(';', 'op'); emit('(', 'op'); emit('__g(),', 'kw'); if (openAfter[i] === 'empty') emit('true', 'id'); i++; continue; }
        if (s === '/') {
          const e = primEnd(i + 1);
          const ls = outChainStart();
          if (isIntRange(out, ls, out.length) && isIntRange(T, sig(i + 1), e)) {
            out.splice(ls, 0, { s: 'Math', t: 'id' }, { s: '.', t: 'op' }, { s: 'trunc', t: 'id' }, { s: '(', t: 'op' });
            emit('/', 'op'); addClose(e, 1);
          } else emit('/', 'op');
          i++; continue;
        }
        if (s === '/=') {
          const p = out.length - 1; let q = p; while (q >= 0 && out[q].t === 'ws') q--;
          if (q >= 0 && out[q].t === 'id' && kindOf(out[q].s) === 'int') {
            const name = out[q].s, e = rhsEnd(i + 1);
            emit(' = ', 'op'); emit('Math', 'id'); emit('.', 'op'); emit('trunc', 'id'); emit('(', 'op'); emit(name, 'id'); emit(' ', 'ws'); emit('/', 'op'); emit(' ', 'ws'); emit('(', 'op'); addClose(e, 2); i++; continue;
          }
          emit('/=', 'op'); i++; continue;
        }
        if (s === '=') {
          let q = out.length - 1; while (q >= 0 && out[q].t === 'ws') q--;
          let r = q - 1; while (r >= 0 && out[r].t === 'ws') r--;
          const isMember = r >= 0 && out[r].t === 'op' && out[r].s === '.';
          if (q >= 0 && out[q].t === 'id' && kindOf(out[q].s) === 'int' && !isMember) {
            const st = sig(i + 1), e = rhsEnd(st);
            const single = e - st <= 2 && T[st].t === 'num' && !T[st].f;
            if (!single) { emit('=', 'op'); emit(' ', 'ws'); emit('Math', 'id'); emit('.', 'op'); emit('trunc', 'id'); emit('(', 'op'); addClose(e, 1); i++; continue; }
          }
          emit('=', 'op'); i++; continue;
        }
        emit(s, 'op'); i++; continue;
      }
      /* identifiers */
      const w = tk.s;
      if (CPP_BAD.has(w)) throw cppErr(tk.line, "'" + w + "' is not supported (the simulator understands functions, variables, arrays and control flow, not classes or templates)");
      if ((CPP_TYPE.has(w) || CPP_QUAL.has(w)) && atStmtStart(i)) {
        let j = i, hasConst = false, hasStatic = false, kind = null, hasType = false;
        while (j < N && T[j].t === 'id' && (CPP_TYPE.has(T[j].s) || CPP_QUAL.has(T[j].s))) {
          const x = T[j].s;
          if (x === 'const' || x === 'constexpr') hasConst = true; if (x === 'static') hasStatic = true;
          if (CPP_TYPE.has(x)) { hasType = true; if (CPP_INT.has(x)) kind = kind || 'int'; else if (CPP_FLOAT.has(x)) kind = 'float'; else if (x === 'String') kind = 'str'; else kind = kind || 'other'; }
          j = sig(j + 1);
        }
        const nm = T[j];
        if (hasType && nm && nm.t === 'op' && (nm.s === '*' || nm.s === '&')) throw cppErr(nm.line, 'pointers and references are not supported');
        if (hasType && nm && nm.t === 'id' && !CPP_TYPE.has(nm.s)) {
          const after = sig(j + 1);
          if (T[after] && T[after].s === '(' && braceDepth === 0) {                 // function definition or prototype
            const close = match(after), nxt = sig(close + 1);
            skipNL(i, j);
            if (T[nxt] && T[nxt].s === ';') { skipNL(j, nxt + 1); i = nxt + 1; continue; }     // prototype: nothing to emit
            const parts = []; let cur = [], d = 0;
            for (let k = after + 1; k < close; k++) {
              const x = T[k]; if (x.t === 'op' && (x.s === '(' || x.s === '[')) d++; if (x.t === 'op' && (x.s === ')' || x.s === ']')) d--;
              if (x.t === 'op' && x.s === ',' && d === 0) { parts.push(cur); cur = []; } else cur.push(x);
            }
            if (cur.some(x => x.t !== 'ws')) parts.push(cur);
            locals = new Map(); const names = [];
            for (const pt of parts) {
              const toks = pt.filter(x => x.t !== 'ws');
              if (toks.length === 1 && toks[0].s === 'void') continue;
              if (toks.some(x => x.s === '*' || x.s === '&')) throw cppErr(toks[0].line, 'pointer and reference parameters are not supported');
              let pk = 'other'; for (const x of toks) { if (CPP_INT.has(x.s)) pk = 'int'; else if (CPP_FLOAT.has(x.s)) pk = 'float'; }
              const eq = toks.findIndex(x => x.s === '='), head = eq < 0 ? toks : toks.slice(0, eq);
              const nameTok = [...head].reverse().find(x => x.t === 'id' && !CPP_TYPE.has(x.s) && !CPP_QUAL.has(x.s));
              if (!nameTok) throw cppErr(toks[0].line, 'a parameter name is missing');
              locals.set(nameTok.s, pk); names.push(nameTok.s + (eq < 0 ? '' : ' = ' + toks.slice(eq + 1).map(x => x.s).join('')));
            }
            emit('function* ' + nm.s + '(' + names.join(', ') + ')', 'op'); skipNL(j, close + 1); i = close + 1; continue;
          }
          if (hasStatic && braceDepth > 0) throw cppErr(tk.line, "'static' local variables are not supported: declare the variable outside the function instead");
          skipNL(i, j);
          emit(hasConst ? 'const ' : 'let ', 'kw');
          const stop = declaratorList(j, kind || 'other', hasConst, tk.line);
          i = stop; continue;
        }
      }
      if (w === 'while' && T[sig(i + 1)] && T[sig(i + 1)].s === '(') guardParen.add(sig(i + 1));
      if (w === 'for' && T[sig(i + 1)] && T[sig(i + 1)].s === '(') {
        const op = sig(i + 1), cl = match(op); let d = 0; const semis = [];
        for (let k = op; k <= cl; k++) { const x = T[k]; if (x.t !== 'op') continue; if (x.s === '(' || x.s === '[' || x.s === '{') d++; else if (x.s === ')' || x.s === ']' || x.s === '}') d--; else if (x.s === ';' && d === 1) semis.push(k); }
        if (semis.length !== 2) throw cppErr(tk.line, "this form of 'for' is not supported (use for (init; condition; step))");
        const empty = T.slice(semis[0] + 1, semis[1]).every(x => x.t === 'ws');
        openAfter[semis[0]] = empty ? 'empty' : 'full'; addClose(semis[1], 1);
        emit('for', 'id'); i++; continue;
      }
      if (w === 'delay' || w === 'delayMicroseconds') {
        const nx = sig(i + 1);
        if (T[nx] && T[nx].s === '(') {
          emit(w === 'delay' ? 'yield ' : 'yield 0.001*', 'kw'); skipNL(i + 1, nx); i = nx; continue;
        }
      }
      if (userFns.has(w) && T[sig(i + 1)] && T[sig(i + 1)].s === '(') {
        const p = sigPrev(i);
        if (!(p >= 0 && isWord(T[p], CPP_TYPE))) {
          if (braceDepth === 0) throw cppErr(tk.line, "calling the function '" + w + "()' outside any function is not supported");
          const nx = sig(i + 1), cl = match(nx);
          emit('(', 'op'); emit('yield* ', 'kw'); emit(w, 'id'); addClose(cl + 1, 1); i++; continue;
        }
      }
      emit(w, 'id'); i++;
    }
    if (closeBefore[b]) { for (let k = 0; k < closeBefore[b]; k++) emit(')', 'op'); delete closeBefore[b]; }
  }

  run(0, N);
  return out.map(e => e.s).join('');
}

if (typeof module !== 'undefined' && module.exports) module.exports = { isCpp, translateCpp };
