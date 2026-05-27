const ICS_URL = process.env.ICS_URL;

const text = await fetch(ICS_URL).then(r => {
  if (!r.ok) throw new Error("Failed to fetch ICS: " + r.status);
  return r.text();
});

// Split into VEVENT blocks
const blocks = text.split("BEGIN:VEVENT").slice(1);

// Minimal parser: pull out DTSTART and SUMMARY (and note all-day)
const events = [];
for (const ch of blocks) {
  const endIdx = ch.indexOf("END:VEVENT");
  const body = endIdx >= 0 ? ch.slice(0, endIdx) : ch;

  // Prefer explicit all-day first
  let allDay = false;
  let startRaw = null;

  const mAll = body.match(/DTSTART;VALUE=DATE:(\d{8})/);
  if (mAll) {
    allDay = true;
    startRaw = mAll[1]; // YYYYMMDD
  } else {
    // Any DTSTART variant, grab value after colon
    const mAny = body.match(/DTSTART(?:;[^:]+)?:([0-9T]+Z?)/);
    if (mAny) startRaw = mAny[1]; // e.g., 20251106T130000Z or 20251106T130000
  }

  const mSum = body.match(/SUMMARY:(.+)/);

  if (startRaw && mSum) {
    events.push({
      summary: mSum[1].trim(),
      startRaw,
      allDay
    });
  }
}

// Write full list; footer will sort/filter client-side in ET.
const fs = await import('node:fs/promises');
await fs.writeFile('assets/events.json', JSON.stringify({ generatedAt: new Date().toISOString(), events }, null, 2));
console.log("Wrote assets/events.json with", events.length, "events");
