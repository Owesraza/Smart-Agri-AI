/**
 * Transliteration Helper for Indian Farmer / User Display Names
 * Converts common English name tokens into Hindi & Marathi (Devanagari script).
 */

const nameMap = {
  // Common First Names
  "owais": { hi: "ओवैस", mr: "ओवैस" },
  "ansari": { hi: "अंसारी", mr: "अंसारी" },
  "bhati": { hi: "भाटी", mr: "भाटी" },
  "suresh": { hi: "सुरेश", mr: "सुरेश" },
  "ramesh": { hi: "रमेश", mr: "रमेश" },
  "vikas": { hi: "विकास", mr: "विकास" },
  "patil": { hi: "पाटिल", mr: "पाटील" },
  "kumar": { hi: "कुमार", mr: "कुमार" },
  "deshmukh": { hi: "देशमुख", mr: "देशमुख" },
  "kiran": { hi: "किरण", mr: "किरण" },
  "amit": { hi: "अमित", mr: "अमित" },
  "sharma": { hi: "शर्मा", mr: "शर्मा" },
  "rajesh": { hi: "राजेश", mr: "राजेश" },
  "pawar": { hi: "पवार", mr: "पवार" },
  "jadhav": { hi: "जाधव", mr: "जाधव" },
  "shinde": { hi: "शिंदे", mr: "शिंदे" },
  "kadam": { hi: "कदम", mr: "कदम" },
  "chavan": { hi: "चव्हण", mr: "चव्हाण" },
  "gaikwad": { hi: "गायकवाड़", mr: "गायकवाड" },
  "agri": { hi: "एग्री", mr: "अ‍ॅग्री" },
  "traders": { hi: "ट्रेडर्स", mr: "ट्रेडर्स" },
  "foods": { hi: "फूड्स", mr: "फूड्स" },
  "pvt": { hi: "प्रा.", mr: "प्रा." },
  "ltd": { hi: "लि.", mr: "लि." },
  "verified": { hi: "सत्यापित", mr: "सत्यापित" },
  "farmer": { hi: "किसान", mr: "शेतकरी" },
  "buyer": { hi: "व्यापारी", mr: "व्यापारी" },
}

export const transliterateName = (nameString, language) => {
  if (!nameString || typeof nameString !== 'string') return nameString || ''
  if (language === 'English' || language === 'en') return nameString

  const langKey = (language === 'Hindi' || language === 'hi') ? 'hi' : 'mr'
  const words = nameString.split(/\s+/)

  const transliteratedWords = words.map(w => {
    const cleanWord = w.toLowerCase().replace(/[^a-z]/g, '')
    if (nameMap[cleanWord] && nameMap[cleanWord][langKey]) {
      return nameMap[cleanWord][langKey]
    }
    return w // Fallback to original word if not in dictionary
  })

  return transliteratedWords.join(' ')
}
