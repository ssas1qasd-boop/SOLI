(function () {
  var toast = document.getElementById('toast');
  var timer;
  function say(msg) {
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout(timer);
    timer = setTimeout(function () { toast.hidden = true; }, 2200);
  }
  function fallback(pre, btn) {
    // Clipboard refused: show the plain code and select it so the reader can copy it by hand.
    pre.hidden = false;
    var range = document.createRange();
    range.selectNodeContents(pre);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    if (ok) { done(btn); }
    else { say('الكود ظاهر ومتحدد تحت الزرار: اضغط نسخ (Copy)'); }
  }
  function done(btn) {
    btn.classList.add('done');
    btn.textContent = '✓ اتنسخ';
    say('اتنسخ الكود كامل. الصقه في الـ compiler وشغّله');
    setTimeout(function () { btn.classList.remove('done'); btn.textContent = '📋 نسخ الكود كامل'; }, 2200);
  }
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button.copy');
    if (!btn) return;
    var pre = document.getElementById(btn.getAttribute('data-src'));
    var text = pre.textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(btn); }, function () { fallback(pre, btn); });
    } else {
      fallback(pre, btn);
    }
  });
  // open the program named in the link (e.g. ...#p1-cpp)
  var id = location.hash.slice(1);
  if (id) { var el = document.getElementById(id); if (el) el.scrollIntoView(); }
})();
