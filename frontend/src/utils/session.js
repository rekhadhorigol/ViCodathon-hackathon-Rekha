export function generateSessionId() {
  // simple UUIDv4-ish generator
  return 'xxxx-4xxx-yxxx-xxxx'.replace(/[xy]/g, function(c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  }).toUpperCase();
}
