declare global {
  interface Window {
    fbq?: (...args: any[]) => void;
    _fbq?: any;
  }
}

export function initMetaPixel(pixelId: string) {
  if (typeof window.fbq !== "undefined") return;

  (function (
    f: Window,
    b: Document,
    e: string,
    v: string,
    n?: any,
    t?: HTMLScriptElement,
    s?: HTMLScriptElement
  ) {
    if (f.fbq) return;

    n = f.fbq = function (...args: any[]) {
      if (n.callMethod) {
        n.callMethod.apply(n, args);
      } else {
        n.queue.push(args);
      }
    };

    if (!f._fbq) f._fbq = n;

    n.push = n;
    n.loaded = true;
    n.version = "2.0";
    n.queue = [];

    t = b.createElement(e) as HTMLScriptElement;
    t.async = true;
    t.src = v;

    s = b.getElementsByTagName(e)[0] as HTMLScriptElement;
    s.parentNode!.insertBefore(t, s);
  })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");

  window.fbq!("init", pixelId);
  window.fbq!("track", "PageView");
}
