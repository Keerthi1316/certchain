import { useEffect, useRef } from 'react';

export default function Stars() {
  const ref = useRef(null);
  useEffect(() => {
    const c = ref.current, x = c.getContext('2d');
    const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let S = [], raf;
    const size = () => {
      c.width = innerWidth; c.height = innerHeight;
      S = Array.from({ length: Math.min(110, innerWidth / 10) }, () => ({
        x: Math.random() * c.width, y: Math.random() * c.height, r: Math.random() * 1.3 + .2, v: Math.random() * .15 + .03, a: Math.random() }));
    };
    const draw = () => {
      x.clearRect(0, 0, c.width, c.height);
      S.forEach((s) => { s.a += .01; s.y -= s.v; if (s.y < 0) s.y = c.height;
        x.globalAlpha = .3 + .5 * Math.abs(Math.sin(s.a)); x.fillStyle = '#cfd4ff'; x.beginPath(); x.arc(s.x, s.y, s.r, 0, 6.3); x.fill(); });
      if (!calm) raf = requestAnimationFrame(draw);
    };
    size(); draw(); addEventListener('resize', size);
    return () => { cancelAnimationFrame(raf); removeEventListener('resize', size); };
  }, []);
  return <><div className="bg" /><canvas id="stars" ref={ref} aria-hidden="true" /></>;
}
