/* "See it run" clip for the simulators. The video file is fetched only when the button is pressed. */
(function () {
  var me = document.currentScript, name = me && me.getAttribute('data-clip'), secs = me && me.getAttribute('data-secs');
  if (!name) return;
  var tries = 0;
  (function place() {
    var pdf = document.querySelector('.pdfx-btn');
    if (!pdf) { if (++tries < 40) setTimeout(place, 100); return; }
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'pdfx-btn be-clip-btn'; b.setAttribute('data-html2canvas-ignore', 'true');
    b.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4L13 8z" fill="currentColor"/></svg><span>See it run &middot; 0:' + secs + '</span>';
    pdf.parentNode.insertBefore(b, pdf);
    b.addEventListener('click', open);
  })();
  function open() {
    var d = document.createElement('dialog'); d.className = 'be-clip'; d.setAttribute('aria-label', 'See it run');
    d.innerHTML = '<video controls autoplay muted playsinline preload="auto" poster="/assets/clips/' + name + '.jpg" src="/assets/clips/' + name + '.mp4"></video>' +
      '<div class="be-clip-foot"><span>Example inputs. Results are hypothetical.</span><button type="button" class="pdfx-btn">Close</button></div>';
    document.body.appendChild(d);
    var close = function () { d.close(); };
    d.querySelector('button').addEventListener('click', close);
    d.addEventListener('click', function (e) { if (e.target === d) close(); });
    d.addEventListener('close', function () { d.remove(); });
    d.showModal ? d.showModal() : d.setAttribute('open', '');
  }
})();
