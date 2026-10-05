"use client";

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { PORTRAITS } from "./about-data";

/** Auto-advancing portrait carousel with manual arrows. */
export function PortraitCarousel({ className = "" }: { className?: string }) {
  const [index, setIndex] = useState(0);
  const count = PORTRAITS.length;

  const go = useCallback(
    (dir: 1 | -1) => setIndex((i) => (i + dir + count) % count),
    [count]
  );

  useEffect(() => {
    const timer = setInterval(() => go(1), 5000);
    return () => clearInterval(timer);
  }, [go, index]); // reset the timer after manual navigation

  return (
    <div
      className={`group relative h-[480px] w-full overflow-hidden rounded-2xl border border-border bg-card shadow-md sm:h-[560px] ${className}`}
    >
      {PORTRAITS.map((p, i) => (
        <Image
          key={p.src}
          src={p.src}
          alt={p.alt}
          fill
          priority={i === 0}
          sizes="(max-width: 640px) 100vw, 320px"
          className={`object-cover transition-opacity duration-500 ${
            i === index ? "opacity-100" : "opacity-0"
          }`}
        />
      ))}

      {/* Arrows */}
      <button
        type="button"
        aria-label="Previous photo"
        onClick={() => go(-1)}
        className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full border border-white/20 bg-black/40 p-2 text-white opacity-0 backdrop-blur transition-opacity focus-visible:opacity-100 group-hover:opacity-100"
      >
        <ChevronLeft className="h-5 w-5" aria-hidden="true" />
      </button>
      <button
        type="button"
        aria-label="Next photo"
        onClick={() => go(1)}
        className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full border border-white/20 bg-black/40 p-2 text-white opacity-0 backdrop-blur transition-opacity focus-visible:opacity-100 group-hover:opacity-100"
      >
        <ChevronRight className="h-5 w-5" aria-hidden="true" />
      </button>

      {/* Dots */}
      <div className="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5">
        {PORTRAITS.map((p, i) => (
          <button
            key={p.src}
            type="button"
            aria-label={`Go to photo ${i + 1}`}
            aria-current={i === index}
            onClick={() => setIndex(i)}
            className={`h-2 rounded-full transition-all ${
              i === index
                ? "w-5 bg-white"
                : "w-2 bg-white/50 hover:bg-white/80"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
