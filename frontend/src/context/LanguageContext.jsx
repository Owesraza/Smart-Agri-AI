import { createContext, useContext, useState, useEffect } from 'react'
import enDict from '../i18n/translations/en.json'
import hiDict from '../i18n/translations/hi.json'
import mrDict from '../i18n/translations/mr.json'
import { transliterateName } from '../i18n/transliterate'
import { mandiTokenMap } from '../i18n/mandiDictionary'

const LanguageContext = createContext(null)

const LANG_KEY = 'smartagri_language'

export const translations = {
  English: enDict,
  Hindi: hiDict,
  Marathi: mrDict,
  en: enDict,
  hi: hiDict,
  mr: mrDict,
}

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem(LANG_KEY) || 'English'
  })

  useEffect(() => {
    localStorage.setItem(LANG_KEY, language)
  }, [language])

  // Helper to resolve nested keys like "dashboard.title" or "crops.onion"
  const t = (path, fallback = '') => {
    if (!path) return fallback
    const currentDict = translations[language] || translations['English']
    const englishDict = translations['English']

    const resolve = (dict, p) => {
      const keys = p.split('.')
      let curr = dict
      for (const k of keys) {
        if (curr && curr[k] !== undefined) {
          curr = curr[k]
        } else {
          return undefined
        }
      }
      return curr
    }

    const val = resolve(currentDict, path)
    if (val !== undefined) return val

    const engVal = resolve(englishDict, path)
    if (engVal !== undefined) return engVal

    return fallback || path
  }

  // Transliterate user names if language is Hindi or Marathi
  const transliterate = (nameStr) => {
    return transliterateName(nameStr, language)
  }

  // Helper to translate backend dynamic status strings
  const translateStatus = (statusStr) => {
    if (!statusStr || typeof statusStr !== 'string') return ''
    const s = statusStr.toLowerCase().trim()
    
    // Order and Delivery Workflow
    if (s === 'delivered' || s.includes('delivery complete') || s === 'closed' || s === 'payment completed') {
      return t('status.delivered', 'Delivered')
    }
    if (s.includes('out for delivery') || s.includes('out_for_delivery')) {
      return t('status.outForDelivery', 'Out for Delivery')
    }
    if (s.includes('dispatch')) {
      return t('status.dispatched', 'Dispatched')
    }
    if (s.includes('order confirmed') || s === 'confirmed' || s.includes('deal confirmed') || s.includes('farmer accepted')) {
      return t('status.orderConfirmed', 'Order Confirmed')
    }
    if (s === 'pending') return t('status.pending', 'Pending')
    if (s === 'accepted') return t('status.accepted', 'Accepted')
    if (s === 'rejected' || s === 'declined') return t('status.rejected', 'Rejected')
    if (s === 'active') return t('status.active', 'Active')
    if (s === 'sold') return t('status.sold', 'Sold')
    if (s === 'cancelled' || s === 'canceled') return t('status.cancelled', 'Cancelled')
    if (s === 'completed') return t('status.completed', 'Completed')
    if (s.includes('transit')) return t('status.inTransit', 'In Transit')
    if (s === 'income') return t('status.income', 'Income')
    if (s === 'expense') return t('status.expense', 'Expense')
    if (s === 'low') return t('status.low', 'Low')
    if (s === 'moderate') return t('status.moderate', 'Moderate')
    if (s === 'high') return t('status.high', 'High')

    const directLookup = t(`status.${s}`)
    if (directLookup && directLookup !== `status.${s}`) return directLookup

    return statusStr
  }

  // Helper to translate weather condition strings from API
  const translateWeather = (conditionStr) => {
    if (!conditionStr || typeof conditionStr !== 'string') return ''
    const c = conditionStr.toLowerCase().trim()
    if (c.includes('clear')) return t('weather.clear', 'Clear Sky')
    if (c.includes('sun')) return t('weather.sunny', 'Sunny')
    if (c.includes('cloud')) return t('weather.clouds', 'Cloudy')
    if (c.includes('thunder') || c.includes('storm')) return t('weather.thunderstorm', 'Thunderstorm')
    if (c.includes('drizzle')) return t('weather.drizzle', 'Drizzle')
    if (c.includes('rain')) return t('weather.rain', 'Rainy')
    if (c.includes('haze')) return t('weather.haze', 'Haze')
    if (c.includes('mist')) return t('weather.mist', 'Mist')
    if (c.includes('fog')) return t('weather.fog', 'Fog')
    return conditionStr
  }

  // Helper to translate day strings
  const translateDay = (dayStr) => {
    if (!dayStr || typeof dayStr !== 'string') return ''
    const d = dayStr.toLowerCase().trim()
    if (d.startsWith('mon')) return t('weather.mon', 'Mon')
    if (d.startsWith('tue')) return t('weather.tue', 'Tue')
    if (d.startsWith('wed')) return t('weather.wed', 'Wed')
    if (d.startsWith('thu')) return t('weather.thu', 'Thu')
    if (d.startsWith('fri')) return t('weather.fri', 'Fri')
    if (d.startsWith('sat')) return t('weather.sat', 'Sat')
    if (d.startsWith('sun')) return t('weather.sun', 'Sun')
    if (d === 'today') return t('weather.today', 'Today')
    if (d === 'tomorrow') return t('weather.tomorrow', 'Tomorrow')
    return dayStr
  }

  // Helper to translate crop names dynamically
  const translateCrop = (cropStr) => {
    if (!cropStr || typeof cropStr !== 'string') return ''
    const clean = cropStr.trim()

    if (language === 'English' || language === 'en') {
      // If crop is passed in Hindi/Marathi, convert back to English
      for (const [enK, hiV] of Object.entries(hiDict.crops || {})) {
        if (clean === hiV) return enDict.crops?.[enK] || enK.charAt(0).toUpperCase() + enK.slice(1)
      }
      for (const [enK, mrV] of Object.entries(mrDict.crops || {})) {
        if (clean === mrV) return enDict.crops?.[enK] || enK.charAt(0).toUpperCase() + enK.slice(1)
      }
      return clean
    }

    const currentDict = (language === 'Hindi' || language === 'hi') ? hiDict : mrDict
    const cropsDict = currentDict?.crops || {}

    const lower = clean.toLowerCase()
    
    // 1. Direct dictionary lookup
    if (cropsDict[lower]) return cropsDict[lower]

    // 2. Normalized underscore lookup (e.g., 'cummin seed' -> 'cummin_seed')
    const under = lower.replace(/[\s\/-]+/g, '_')
    if (cropsDict[under]) return cropsDict[under]

    // 3. Normalized space lookup (e.g., 'cummin_seed' -> 'cummin seed')
    const spaced = lower.replace(/[_/-]+/g, ' ')
    if (cropsDict[spaced]) return cropsDict[spaced]

    // 4. Remove parenthetical info (e.g. "Groundnut (Peanut)" -> "groundnut")
    const baseWord = lower.replace(/\s*\([^)]*\)/g, '').trim()
    if (cropsDict[baseWord]) return cropsDict[baseWord]
    const baseUnder = baseWord.replace(/[\s\/-]+/g, '_')
    if (cropsDict[baseUnder]) return cropsDict[baseUnder]

    // 5. First word lookup (e.g. "Apple Golden" -> "apple")
    const firstWord = baseWord.split(/[\s_/-]+/)[0]
    if (cropsDict[firstWord]) return cropsDict[firstWord]

    return clean
  }

  // Mandi & Location mapping table
  const mandiMap = {
    "pune": { hi: "पुणे", mr: "पुणे" },
    "moshi": { hi: "मोशी", mr: "मोशी" },
    "nashik": { hi: "नासिक", mr: "नाशिक" },
    "nasik": { hi: "नासिक", mr: "नाशिक" },
    "nagpur": { hi: "नागपुर", mr: "नागपूर" },
    "mumbai": { hi: "मुंबई", mr: "मुंबई" },
    "vashi": { hi: "वाशी", mr: "वाशी" },
    "amravati": { hi: "अमरावती", mr: "अमरावती" },
    "kolhapur": { hi: "कोल्हापुर", mr: "कोल्हापूर" },
    "solapur": { hi: "सोलापुर", mr: "सोलापूर" },
    "aurangabad": { hi: "छत्रपति संभाजीनगर", mr: "छत्रपती संभाजीनगर" },
    "sambhajinagar": { hi: "संभाजीनगर", mr: "संभाजीनगर" },
    "chhatrapati": { hi: "छत्रपति", mr: "छत्रपती" },
    "chattrapati": { hi: "छत्रपति", mr: "छत्रपती" },
    "ahmednagar": { hi: "अहमदनगर", mr: "अहमदनगर" },
    "jalgaon": { hi: "जलगांव", mr: "जळगाव" },
    "dhule": { hi: "धुले", mr: "धुळे" },
    "satara": { hi: "सतारा", mr: "सातारा" },
    "sangli": { hi: "सांगली", mr: "सांगली" },
    "nanded": { hi: "नांदेड़", mr: "नांदेड" },
    "latur": { hi: "लातूर", mr: "लातूर" },
    "akola": { hi: "अकोला", mr: "अकोला" },
    "baramati": { hi: "बारामती", mr: "बारामती" },
    "lasalgaon": { hi: "लासलगांव", mr: "लासलगाव" },
    "pimpalgaon": { hi: "पिंपलगांव", mr: "पिंपळगाव" },
    "kalyan": { hi: "कल्याण", mr: "कल्याण" },
    "junnar": { hi: "जुन्नर", mr: "जुन्नर" },
    "alephata": { hi: "आलेफाटा", mr: "आलेफाटा" },
    "yeola": { hi: "येवला", mr: "येवला" },
    "sinnar": { hi: "सिन्नर", mr: "सिन्नर" },
    "kalvan": { hi: "कलवण", mr: "कलवण" },
    "dindori": { hi: "दिंडोरी", mr: "दिंडोरी" },
    "manmad": { hi: "मनमाड", mr: "मनमाड" },
    "chandwad": { hi: "चांदवड", mr: "चांदवड" },
    "karad": { hi: "कराड", mr: "कराड" },
    "phaltan": { hi: "फलटण", mr: "फलटण" },
    "wai": { hi: "वाई", mr: "वाई" },
    "maharashtra": { hi: "महाराष्ट्र", mr: "महाराष्ट्र" },
    "apmc": { hi: "एपीएमसी", mr: "एपीएमसी" },
    "mandi": { hi: "मंडी", mr: "मंडी" },
    "market": { hi: "बाजार", mr: "बाजार" },
    "yard": { hi: "यार्ड", mr: "यार्ड" },
    "sub-yard": { hi: "उप-यार्ड", mr: "उप-यार्ड" },
    "main": { hi: "मुख्य", mr: "मुख्य" },
  }

  // Helper to translate Mandi / APMC names
  const translateMandi = (mandiStr) => {
    if (!mandiStr || typeof mandiStr !== 'string') return ''
    if (language === 'English' || language === 'en') return mandiStr

    const targetLang = (language === 'Hindi' || language === 'hi') ? 'hi' : 'mr'

    // Handle parentheses like "Chandrapur (Ganjwad)" or "Junnar (Alephata)" or "Pune(Moshi)"
    let out = mandiStr.replace(/\s*\(([^)]+)\)/g, (match, inner) => {
      const innerTokens = inner.split(/[\s,\-]+/).filter(Boolean)
      const transInner = innerTokens.map(w => {
        const cl = w.toLowerCase().replace(/[^a-z0-9]/g, '')
        if (mandiTokenMap && mandiTokenMap[cl] && mandiTokenMap[cl][targetLang]) return mandiTokenMap[cl][targetLang]
        if (mandiMap[cl] && mandiMap[cl][targetLang]) return mandiMap[cl][targetLang]
        return transliterate(w)
      }).join(' ')
      return ` (${transInner})`
    })

    // Replace English tokens using mandiTokenMap and mandiMap, with transliterate fallback
    out = out.replace(/[a-zA-Z]+/g, (word) => {
      const clean = word.toLowerCase()
      if (mandiTokenMap && mandiTokenMap[clean] && mandiTokenMap[clean][targetLang]) {
        return mandiTokenMap[clean][targetLang]
      }
      if (mandiMap[clean] && mandiMap[clean][targetLang]) {
        return mandiMap[clean][targetLang]
      }
      return transliterate(word)
    })

    return out
  }

  // Helper to translate comma-separated crop lists (e.g. "Wheat, Onion, Tomato")
  const translateCropsList = (cropsStr) => {
    if (!cropsStr || typeof cropsStr !== 'string') return ''
    if (language === 'English' || language === 'en') return cropsStr

    const items = cropsStr.split(',').map(s => s.trim())
    const translated = items.map(c => translateCrop(c))
    return translated.join(', ')
  }

  // Helper to translate capacity strings (e.g. "200 Quintals" -> "200 कुंतल")
  const translateCapacity = (capStr) => {
    if (!capStr || typeof capStr !== 'string') return ''
    if (language === 'English' || language === 'en') return capStr

    const unitLabel = t('units.quintal', 'कुंतल')
    return capStr
      .replace(/\bQuintals\b/gi, unitLabel)
      .replace(/\bQuintal\b/gi, unitLabel)
      .replace(/\bQtl\b/gi, unitLabel)
      .replace(/\bTonnes\b/gi, t('units.tonne', 'टन'))
      .replace(/\bTonne\b/gi, t('units.tonne', 'टन'))
      .replace(/\bKg\b/gi, t('units.kg', 'किलो'))
  }

  return (
    <LanguageContext.Provider value={{
      language,
      setLanguage,
      t,
      transliterate,
      translateStatus,
      translateWeather,
      translateDay,
      translateCrop,
      translateCropsList,
      translateCapacity,
      translateMandi,
      useTranslation: () => ({ t, language, setLanguage, transliterate, translateStatus, translateWeather, translateDay, translateCrop, translateCropsList, translateCapacity, translateMandi })
    }}>
      {children}
    </LanguageContext.Provider>
  )
}

export const useLanguage = () => {
  const ctx = useContext(LanguageContext)
  if (!ctx) {
    return {
      language: 'English',
      setLanguage: () => {},
      t: (path, fallback = '') => fallback || path,
      transliterate: (str) => str,
      translateStatus: (s) => s,
      translateWeather: (w) => w,
      translateDay: (d) => d,
      translateCrop: (c) => c,
      translateCropsList: (cs) => cs,
      translateCapacity: (cap) => cap,
      translateMandi: (m) => m,
    }
  }
  return ctx
}

export const useTranslation = () => {
  const ctx = useContext(LanguageContext)
  if (!ctx) {
    return {
      language: 'English',
      setLanguage: () => {},
      t: (path, fallback = '') => fallback || path,
      transliterate: (str) => str,
      translateStatus: (s) => s,
      translateWeather: (w) => w,
      translateDay: (d) => d,
      translateCrop: (c) => c,
      translateCropsList: (cs) => cs,
      translateCapacity: (cap) => cap,
      translateMandi: (m) => m,
    }
  }
  return {
    t: ctx.t,
    language: ctx.language,
    setLanguage: ctx.setLanguage,
    transliterate: ctx.transliterate,
    translateStatus: ctx.translateStatus,
    translateWeather: ctx.translateWeather,
    translateDay: ctx.translateDay,
    translateCrop: ctx.translateCrop,
    translateCropsList: ctx.translateCropsList,
    translateCapacity: ctx.translateCapacity,
    translateMandi: ctx.translateMandi
  }
}

export default LanguageContext
