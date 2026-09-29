import { useState, useEffect, useMemo } from 'react'
import axiosClient from '../api/axiosClient'
import TimelineItem from '../components/TimelineItem'
import TaskCard from '../components/TaskCard'
import Card, { CardHeader } from '../components/Card'
import { useLanguage } from '../context/LanguageContext'

const Workflow = () => {
  const { t, language, translateCrop, translateStatus } = useLanguage()
  const [activeTab, setActiveTab] = useState('lifecycle') // 'lifecycle' | 'deals'
  const [selectedCrop, setSelectedCrop] = useState('All')
  const [tasks, setTasks] = useState([])
  const [deals, setDeals] = useState([])
  const [plots, setPlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [aiGenerating, setAiGenerating] = useState(false)
  const [toastMessage, setToastMessage] = useState(null)

  // Dynamically derive crop filter options STRICTLY from crops entered by the farmer in Plot Management
  const farmerCrops = useMemo(() => {
    const cropSet = new Set()

    // 1. Primary: Extract crops strictly from Plot Management
    if (Array.isArray(plots) && plots.length > 0) {
      plots.forEach(p => {
        const cName = p.crop_name || p.crop || ''
        if (cName.trim()) cropSet.add(cName.trim())
      })
    } else {
      // 2. Fallback only if farmer has 0 plots registered yet
      if (Array.isArray(tasks)) {
        tasks.forEach(t => {
          const cName = t.crop || ''
          if (cName.trim()) cropSet.add(cName.trim())
        })
      }
    }

    const emojiMap = {
      Onion: '🧅',
      Wheat: '🌾',
      Tomato: '🍅',
      Grapes: '🍇',
      Cotton: '☁️',
      Maize: '🌽',
      Soybean: '🫘',
      Potato: '🥔',
      Rice: '🌾',
      Sugarcane: '🎋',
      Pomegranate: '🍎'
    }

    const result = []
    cropSet.forEach(c => {
      const icon = emojiMap[c] || '🌱'
      result.push({ id: c, label: `${icon} ${translateCrop ? translateCrop(c) : c}` })
    })

    return result
  }, [plots, tasks, language, translateCrop])

  useEffect(() => {
    if (farmerCrops.length > 0 && (!selectedCrop || selectedCrop === 'All')) {
      setSelectedCrop(farmerCrops[0].id)
    }
  }, [farmerCrops])

  const CROP_STAGE_DESCRIPTIONS = {
    Onion: {
      1: 'Deep field tillage, FYM organic manure application (15-20 T/ha), and soil pH testing (6.5-7.5).',
      2: '45-day nursery bed transplanting with certified seeds (AFR/NHRDF-Red) at 15cm x 10cm spacing.',
      3: 'Drip line fertigation setup, split NPK (100:50:50) dosing, and elemental sulfur top dressing.',
      4: 'Thrips pest inspection, bio-pesticide spray (Azadirachtin), and purple blotch fungicide application.',
      5: 'Top neck fall harvest, field shade curing (10-15 days), and A/B export grade classification.',
      6: 'Ventilated red mesh bag packing (50kg) and dispatch to Lasalgaon APMC auction.'
    },
    Wheat: {
      1: 'Rotavator ploughing, laser land leveling, and pre-sowing Palewa irrigation.',
      2: 'HD-2967 / GW-322 certified seed treatment (Tebuconazole) and seed drill line sowing.',
      3: 'Crown Root Initiation (CRI) irrigation at 21 days and DAP/Urea split top dressing.',
      4: 'Yellow rust & leaf blight inspection, Phalaris minor weedicide spray.',
      5: 'Combine harvesting at 12-14% grain moisture level and cleaning/bagging.',
      6: 'Mandi transport to APMC, MSP procurement auction, and direct ledger credit.'
    },
    Tomato: {
      1: 'Raised bed preparation (4ft width), silver-black mulching sheet laying, and basal dosing.',
      2: 'Hybrid seedling transplanting (Arka Rakshak) with drip emitters at 60cm spacing.',
      3: 'Bamboo staking & wire trellising setup, NPK (19:19:19) fertigation schedule.',
      4: 'Fruit borer pheromone traps, whitefly control spray, and Calcium nitrate application.',
      5: 'Selective Breaker-stage harvesting and plastic crate sorting by color/size.',
      6: 'Transport in ventilated plastic crates to regional APMC Mandi.'
    },
    Grapes: {
      1: 'April back-pruning (Foundation pruning), cane development, and subsoil aeration.',
      2: 'October forward pruning, flower cluster thinning, and GA3 gibberellic acid dipping.',
      3: 'Micro-drip fertigation with Potassium & Magnesium sulphate for berry sizing.',
      4: 'Downy mildew & powdery mildew canopy spray, Mealybug bio-control.',
      5: 'Brix sweetness testing (18-20° Brix harvest), manual cluster trimming, and punnet packing.',
      6: 'Cold chain refrigerated transport to cold storage or export packhouse.'
    },
    Cotton: {
      1: 'Deep summer ploughing, ridges & furrows formation, and FYM compost application.',
      2: 'Bt-Cotton hybrid seed dibbling at 90cm x 60cm spacing with seed treatment.',
      3: 'Inter-cultivation weeding, Drip fertigation, and Potassium nitrate foliar spray.',
      4: 'Pink bollworm monitoring, ETL-based bio-spray, and sucking pest management.',
      5: 'Phase-wise manual boll picking, sun-drying, and trash separation.',
      6: 'Balering transport to local cotton ginning factory or APMC market.'
    }
  }

  const CROP_STAGE_TASKS = {
    Cotton: {
      1: ['Deep Summer Soil Preparation', 'FYM Compost Mixing', 'Field Leveling & Furrows'],
      2: ['Bt-Cotton Seed Dibbling', 'Refuge Row Sowing', 'Seed Treatment & Soil Test'],
      3: ['Inter-cultivation Weeding', 'Drip Fertigation (19:19:19)', 'Potassium Foliar Spray'],
      4: ['Pink Bollworm Inspection', 'Pheromone Trap Installation', 'Bio-Insecticide Spray'],
      5: ['Phase-1 Manual Boll Picking', 'Sun Drying & Trash Removal', 'Grade-A Fiber Classification'],
      6: ['Ginning Factory Dispatch', 'Cotton Bale Haulage', 'Ledger Settlement']
    },
    Onion: {
      1: ['Deep Field Tillage', 'FYM Compost Application', 'Soil pH Testing'],
      2: ['Nursery Bed Seed Sowing', '45-Day Seedling Transplanting', 'Line Spacing Check'],
      3: ['Drip Fertigation Setup', 'Split NPK Application', 'Elemental Sulfur Dosing'],
      4: ['Thrips Inspection', 'Azadirachtin Bio-Spray', 'Purple Blotch Fungicide'],
      5: ['Top Neck Fall Harvesting', 'Shade Field Curing (10-15 Days)', 'A/B Export Size Grading'],
      6: ['Ventilated Mesh Bag Packing', 'Lasalgaon APMC Transport', 'Auction & Payment Settlement']
    },
    Wheat: {
      1: ['Rotavator Tillage', 'Laser Land Leveling', 'Palewa Pre-sowing Irrigation'],
      2: ['Certified Seed Treatment', 'Seed Drill Line Sowing', 'Soil Depth Check'],
      3: ['Crown Root Initiation Irrigation', 'Urea Split Top Dressing', 'NPK Fertigation'],
      4: ['Yellow Rust Inspection', 'Leaf Blight Protection Spray', 'Phalaris Weed Control'],
      5: ['Grain Moisture Level Test', 'Combine Harvester Operation', '50kg Bagging & Cleaning'],
      6: ['APMC Mandi Haulage', 'MSP Procurement Auction', 'Bank Ledger Settlement']
    },
    Tomato: {
      1: ['Raised Bed Preparation', 'Mulching Sheet Laying', 'Basal Fertilizer Dosing'],
      2: ['Hybrid Seedling Transplanting', 'Drip Inline Emitter Test', 'Root Zone Drenching'],
      3: ['Bamboo Staking Setup', 'Wire Trellising & Tying', 'NPK (19:19:19) Fertigation'],
      4: ['Fruit Borer Pheromone Traps', 'Whitefly Spray', 'Calcium Nitrate Spray'],
      5: ['Breaker Stage Harvesting', 'Plastic Crate Sorting', 'Color & Size Grading'],
      6: ['Ventilated Crate Transport', 'APMC Mandi Dispatch', 'Payment Collection']
    },
    Grapes: {
      1: ['April Foundation Back-Pruning', 'Cane Development Check', 'Subsoil Aeration'],
      2: ['October Forward Pruning', 'Cluster Thinning', 'GA3 Dip Application'],
      3: ['Potassium Fertigation', 'Magnesium Sulphate Dosing', 'Berry Sizing Inspection'],
      4: ['Downy Mildew Canopy Spray', 'Powdery Mildew Control', 'Mealybug Bio-Control'],
      5: ['Brix Sweetness Testing (18-20°)', 'Manual Cluster Trimming', 'Punnet Packing'],
      6: ['Refrigerated Cold Chain Haulage', 'Cold Storage Dispatch', 'Export Settlement']
    }
  }

  // Filter tasks dynamically based on selected crop button
  const filteredTasks = useMemo(() => {
    if (selectedCrop === 'All') return tasks
    return tasks.filter(t => (t.crop || '').toLowerCase().includes(selectedCrop.toLowerCase()))
  }, [tasks, selectedCrop])

  // Find active plot object corresponding to selected crop to extract sowing_date and expected_harvest
  const activePlotForCrop = useMemo(() => {
    if (!Array.isArray(plots) || plots.length === 0) return null
    if (selectedCrop === 'All') return plots[0]
    return plots.find(p => (p.crop_name || p.crop || '').toLowerCase().includes(selectedCrop.toLowerCase())) || plots[0]
  }, [plots, selectedCrop])

  // Dynamic individual tasks display for selected crop
  const displayTasks = useMemo(() => {
    if (filteredTasks.length > 0) return filteredTasks

    // Fallback: If 0 DB tasks exist for selected crop, construct individual tasks for that crop
    const targetCrop = selectedCrop === 'All' ? (activePlotForCrop?.crop_name || 'Cotton') : selectedCrop
    const cropTasksObj = CROP_STAGE_TASKS[targetCrop] || CROP_STAGE_TASKS['Cotton']
    const generated = []
    let idCounter = 1

    const stageNames = {
      1: 'Soil Prep',
      2: 'Sowing',
      3: 'Irrigation',
      4: 'Pest Control',
      5: 'Harvesting',
      6: 'Mandi Sale'
    }

    Object.keys(cropTasksObj).forEach(stageId => {
      const stageTasksList = cropTasksObj[stageId]
      stageTasksList.forEach(taskTitle => {
        generated.push({
          id: `virtual-${targetCrop}-${idCounter++}`,
          title: taskTitle,
          status: 'Pending',
          priority: 'High',
          dueDate: getStageDateFromPlot(parseInt(stageId), '2026-08-24'),
          crop: targetCrop,
          description: `${targetCrop} ${stageNames[stageId] || 'Stage'} Action Task`
        })
      })
    })

    return generated
  }, [filteredTasks, selectedCrop, activePlotForCrop])

  // Add Task Modal
  const [showTaskModal, setShowTaskModal] = useState(false)
  const [newTask, setNewTask] = useState({
    title: '',
    task_type: 'Soil Prep',
    description: '',
    due_date: new Date().toISOString().split('T')[0],
    priority: 'Medium',
    crop: 'Wheat'
  })

  // Deal Step Update Modal
  const [selectedDeal, setSelectedDeal] = useState(null)
  const [showDealModal, setShowDealModal] = useState(false)
  const [dealNewStatus, setDealNewStatus] = useState('Harvest Scheduled')
  const [transportCost, setTransportCost] = useState(0)
  const [packagingCost, setPackagingCost] = useState(0)
  const [updatingDeal, setUpdatingDeal] = useState(false)

  const showToast = (msg, type = 'success') => {
    setToastMessage({ text: msg, type })
    setTimeout(() => setToastMessage(null), 3000)
  }

  // Helper to interpolate stage dates dynamically based on sowing_date and expected_harvest
  function getStageDateFromPlot(stageId, defaultDateStr) {
    if (!activePlotForCrop || !activePlotForCrop.sowing_date) return defaultDateStr

    try {
      const sowDt = new Date(activePlotForCrop.sowing_date)
      if (isNaN(sowDt.getTime())) return defaultDateStr

      let harvestDt
      if (activePlotForCrop.expected_harvest) {
        harvestDt = new Date(activePlotForCrop.expected_harvest)
      } else {
        harvestDt = new Date(sowDt.getTime() + 100 * 24 * 60 * 60 * 1000)
      }
      if (isNaN(harvestDt.getTime())) {
        harvestDt = new Date(sowDt.getTime() + 100 * 24 * 60 * 60 * 1000)
      }

      const totalMs = harvestDt.getTime() - sowDt.getTime()
      const totalDays = Math.max(10, Math.round(totalMs / (1000 * 60 * 60 * 24)))

      let targetDt = new Date(sowDt.getTime())

      if (stageId === 1) {
        targetDt.setDate(targetDt.getDate() - 7)
      } else if (stageId === 2) {
        targetDt = new Date(sowDt.getTime())
      } else if (stageId === 3) {
        targetDt.setDate(targetDt.getDate() + Math.round(totalDays * 0.20))
      } else if (stageId === 4) {
        targetDt.setDate(targetDt.getDate() + Math.round(totalDays * 0.50))
      } else if (stageId === 5) {
        targetDt = new Date(harvestDt.getTime())
      } else if (stageId === 6) {
        targetDt = new Date(harvestDt.getTime())
        targetDt.setDate(targetDt.getDate() + 7)
      }

      return targetDt.toISOString().split('T')[0]
    } catch (e) {
      return defaultDateStr
    }
  }

  // Dynamically calculate Seasonal Timeline steps based on active database tasks, selected crop, and plot sowing/harvest dates
  const timelineSteps = useMemo(() => {
    const stages = [
      { id: 1, title: 'Soil & Land Preparation', keywords: ['soil', 'land', 'plough', 'compost', 'prep'], defaultDate: '2026-08-01' },
      { id: 2, title: 'Seed Selection & Sowing', keywords: ['seed', 'sow', 'plant', 'variety', 'nursery'], defaultDate: '2026-08-05' },
      { id: 3, title: 'Irrigation & Nutrient Management', keywords: ['irrigat', 'water', 'fertiliz', 'dap', 'urea', 'npk', 'top dressing'], defaultDate: '2026-08-15' },
      { id: 4, title: 'Pest & Plant Health Protection', keywords: ['pest', 'spray', 'insect', 'fungi', 'weed', 'protect'], defaultDate: '2026-08-25' },
      { id: 5, title: 'Harvesting & Quality Grading', keywords: ['harvest', 'grad', 'pack', 'sort', 'curing'], defaultDate: '2026-09-10' },
      { id: 6, title: 'Mandi Sale & Payment Settlement', keywords: ['market', 'mandi', 'auct', 'sale', 'pay', 'transport', 'deal'], defaultDate: '2026-09-20' }
    ]

    const targetCrop = selectedCrop === 'All' ? (activePlotForCrop?.crop_name || 'Cotton') : selectedCrop
    const defaultCropTasks = CROP_STAGE_TASKS[targetCrop] || CROP_STAGE_TASKS['Cotton']

    return stages.map(stage => {
      const matchingTasks = filteredTasks.filter(t => {
        const titleLower = (t.title || '').toLowerCase()
        const descLower = (t.description || '').toLowerCase()
        return stage.keywords.some(kw => titleLower.includes(kw) || descLower.includes(kw))
      })

      let status = 'Upcoming'
      let date = getStageDateFromPlot(stage.id, stage.defaultDate)
      let taskList = matchingTasks.map(t => t.title)

      if (matchingTasks.length > 0) {
        const completedCount = matchingTasks.filter(t => t.status === 'Completed').length
        date = matchingTasks[0].dueDate || date
        if (completedCount === matchingTasks.length) {
          status = 'Completed'
        } else {
          status = 'In Progress'
        }
      } else {
        // Use individual crop action tasks
        taskList = defaultCropTasks[stage.id] || [`${targetCrop} Stage Guidelines`]
      }

      const cropDesc = (CROP_STAGE_DESCRIPTIONS[targetCrop] && CROP_STAGE_DESCRIPTIONS[targetCrop][stage.id])
        ? CROP_STAGE_DESCRIPTIONS[targetCrop][stage.id]
        : (stage.id === 1 ? 'Field tillage, organic manure application, and soil testing.' :
           stage.id === 2 ? 'Certified seed treatment and row sowing at ideal depth.' :
           stage.id === 3 ? 'Drip line setup, crown root irrigation, and NPK fertilizer application.' :
           stage.id === 4 ? 'Proactive inspection, bio-pesticide spray, and weed removal.' :
           stage.id === 5 ? 'Crop harvesting, mesh bag packing, and A/B grade classification.' :
           'Early morning transport to APMC mandi, auction sale, and ledger settlement.')

      return {
        id: stage.id,
        title: stage.title,
        status: status,
        date: date,
        description: cropDesc,
        tasks: taskList
      }
    })
  }, [filteredTasks, selectedCrop, activePlotForCrop])

  // Load Real Workflow Tasks & Deals from SQL Database
  const fetchWorkflowData = async () => {
    setLoading(true)
    try {
      // 1. Fetch Real Database Tasks
      const resTasks = await axiosClient.get('/api/v1/workflow/')
      if (resTasks.data && resTasks.data.success && Array.isArray(resTasks.data.data)) {
        const mapped = resTasks.data.data.map(t => ({
          id: t.id,
          title: t.title,
          status: t.status || 'Pending',
          priority: t.priority || 'Medium',
          dueDate: t.due_date || t.created_at?.split('T')[0] || '2026-08-10',
          crop: t.crop || 'Wheat',
          description: t.description
        }))
        setTasks(mapped)
      }

      // 2. Fetch Real User Deals Workflow
      const resDeals = await axiosClient.get('/api/v1/deals/my')
      if (resDeals.data && resDeals.data.success && Array.isArray(resDeals.data.data)) {
        setDeals(resDeals.data.data)
      }

      // 3. Fetch Real User Plots from Plot Management
      const resPlots = await axiosClient.get('/api/v1/plots/')
      if (resPlots.data && resPlots.data.success && Array.isArray(resPlots.data.data)) {
        setPlots(resPlots.data.data)
      }
    } catch (err) {
      console.warn('Error loading workflow data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWorkflowData()
  }, [])

  // Toggle Task Status (Pending <-> Completed) and Sync with SQL DB
  const toggleTask = async (taskId) => {
    let target = tasks.find(t => t.id === taskId)
    let isVirtual = false

    if (!target) {
      target = displayTasks.find(t => t.id === taskId)
      if (target) isVirtual = true
    }

    if (!target) return

    const newStatus = target.status === 'Completed' ? 'Pending' : 'Completed'

    if (isVirtual) {
      const updatedVirtual = { ...target, status: newStatus }
      setTasks(prev => [updatedVirtual, ...prev])

      try {
        const res = await axiosClient.post('/api/v1/workflow/', {
          title: target.title,
          task_type: 'Crop Action',
          description: target.description || `${target.crop} Task`,
          due_date: target.dueDate || new Date().toISOString().split('T')[0],
          priority: target.priority || 'High',
          crop: target.crop
        })
        if (res.data?.success && res.data?.data) {
          const createdId = res.data.data.id
          await axiosClient.patch(`/api/v1/workflow/${createdId}/status`, { status: newStatus })
          setTasks(prev => prev.map(t => t.id === target.id ? { ...t, id: createdId } : t))
        }
        showToast(`Task marked as ${newStatus}`)
      } catch (err) {
        console.warn('Failed to save virtual task to DB:', err)
      }
    } else {
      setTasks(prev => prev.map(t => t.id === taskId ? { ...t, status: newStatus } : t))

      try {
        await axiosClient.patch(`/api/v1/workflow/${taskId}/status`, { status: newStatus })
        showToast(`Task marked as ${newStatus}`)
      } catch (err) {
        console.warn('Failed to update task status in DB:', err)
        setTasks(prev => prev.map(t => t.id === taskId ? { ...t, status: target.status } : t))
        showToast('Could not sync task status', 'error')
      }
    }
  }

  // Handle Add Custom Task
  const handleCreateTask = async (e) => {
    e.preventDefault()
    if (!newTask.title.trim()) return

    try {
      const res = await axiosClient.post('/api/v1/workflow/', newTask)
      if (res.data && res.data.success) {
        showToast('✅ Workflow task added to database!')
        setShowTaskModal(false)
        setNewTask({
          title: '',
          task_type: 'Soil Prep',
          description: '',
          due_date: new Date().toISOString().split('T')[0],
          priority: 'Medium',
          crop: 'Wheat'
        })
        fetchWorkflowData()
      }
    } catch (err) {
      console.error('Error creating task:', err)
      showToast('Failed to create task', 'error')
    }
  }

  const [showAiModal, setShowAiModal] = useState(false)
  const [aiForm, setAiForm] = useState({
    crop: 'Wheat',
    quantity: 100,
    mandi: 'Nashik APMC',
  })

  // Handle AI Automated Workflow Generation
  const handleGenerateAiWorkflow = async (e) => {
    if (e) e.preventDefault()
    setAiGenerating(true)
    try {
      let aiSteps = []
      try {
        const res = await axiosClient.post('/api/v1/ai/workflow', {
          crop: aiForm.crop,
          quantity: parseFloat(aiForm.quantity) || 100,
          mandi: aiForm.mandi,
          recommendation: 'SELL'
        })
        const stepsData = res.data?.data
        if (Array.isArray(stepsData) && stepsData.length > 0) {
          aiSteps = stepsData
        } else if (stepsData?.steps && Array.isArray(stepsData.steps)) {
          aiSteps = stepsData.steps
        }
      } catch (aiErr) {
        console.warn('AI endpoint fallback active:', aiErr)
      }

      // If AI service offline or fallback needed, create 5-stage crop workflow
      if (aiSteps.length === 0) {
        const today = new Date().toISOString().split('T')[0]
        aiSteps = [
          { task: `Soil & Land Prep for ${aiForm.crop}`, description: 'Deep plowing, organic manure mixing, and soil testing.', priority: 'High', date: today },
          { task: `Seed Sowing & Treatment for ${aiForm.crop}`, description: 'Certified seed treatment and row sowing at ideal depth.', priority: 'High', date: today },
          { task: `Irrigation & Fertilizer Schedule`, description: 'Drip line setup, crown root irrigation, and NPK application.', priority: 'High', date: today },
          { task: `Pest Protection Spray`, description: 'Proactive bio-pesticide spray and weed control.', priority: 'Medium', date: today },
          { task: `Harvesting & ${aiForm.mandi || 'Mandi'} Dispatch`, description: `Harvest produce, pack in mesh bags, and transport to ${aiForm.mandi || 'mandi'}.`, priority: 'High', date: today }
        ]
      }

      // Save all tasks into DB and collect creation responses
      const createdResponses = await Promise.all(
        aiSteps.map(step =>
          axiosClient.post('/api/v1/workflow/', {
            title: step.task || step.title || step.step || `${aiForm.crop} Stage Task`,
            task_type: 'AI Lifecycle',
            description: step.description || `AI Recommended step for ${aiForm.crop}`,
            due_date: step.date || step.due_date || new Date().toISOString().split('T')[0],
            priority: step.priority || 'High',
            crop: aiForm.crop
          }).catch(err => console.warn('Failed single step post:', err))
        )
      )

      // Instantly map created tasks into UI state for zero-latency display
      const newCreatedTasks = createdResponses
        .filter(r => r?.data?.success && r?.data?.data)
        .map(r => {
          const t = r.data.data
          return {
            id: t.id,
            title: t.title,
            status: t.status || 'Pending',
            priority: t.priority || 'High',
            dueDate: t.due_date || new Date().toISOString().split('T')[0],
            crop: t.crop || aiForm.crop,
            description: t.description
          }
        })

      if (newCreatedTasks.length > 0) {
        setTasks(prev => [...newCreatedTasks, ...prev])
      }

      showToast(`🚀 AI Lifecycle Workflow for ${aiForm.crop} generated and saved to your database!`)
      setShowAiModal(false)
      fetchWorkflowData()
    } catch (err) {
      console.error('Error generating AI workflow:', err)
      showToast('Failed to generate AI workflow', 'error')
    } finally {
      setAiGenerating(false)
    }
  }

  // Handle Deal Status Advancement
  const handleAdvanceDealStatus = async (e) => {
    e.preventDefault()
    if (!selectedDeal) return

    setUpdatingDeal(true)
    try {
      const res = await axiosClient.patch(`/api/v1/deals/${selectedDeal.id}/status`, {
        new_status: dealNewStatus,
        transport_cost: parseFloat(transportCost) || 0,
        packaging_cost: parseFloat(packagingCost) || 0
      })

      if (res.data && res.data.success) {
        showToast(`🎉 Deal advanced to '${dealNewStatus}'! ${dealNewStatus.toLowerCase().includes('payment') ? 'Ledger automatically updated!' : ''}`)
        setShowDealModal(false)
        setSelectedDeal(null)
        fetchWorkflowData()
      }
    } catch (err) {
      console.error('Error advancing deal status:', err)
      showToast('Failed to update deal workflow', 'error')
    } finally {
      setUpdatingDeal(false)
    }
  }

  const completedTasksCount = displayTasks.filter(t => t.status === 'Completed').length
  const progressPercent = displayTasks.length > 0 ? Math.round((completedTasksCount / displayTasks.length) * 100) : 0

  return (
    <div className="space-y-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-xl shadow-xl text-xs font-bold transition-all ${
          toastMessage.type === 'error' ? 'bg-red-600 text-white' : 'bg-emerald-700 text-white'
        }`}>
          {toastMessage.text}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap bg-white p-6 rounded-2xl border border-gray-100 shadow-xs">
        <div>
          <h1 className="text-2xl font-extrabold text-gray-900">{t('workflow.title', 'Crop & Deal Workflow Engine')}</h1>
          <p className="text-gray-500 text-xs mt-1">Track seasonal crop lifecycle tasks, database workflow milestones, and active marketplace deal stages.</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowTaskModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all cursor-pointer shadow-sm flex items-center gap-1.5"
          >
            <span>➕</span> Add Task
          </button>
        </div>
      </div>

      {/* CROP LIFECYCLE & TASKS */}
      <div className="space-y-6">
          {/* Interactive Crop Selection Bar */}
          <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-xs flex flex-wrap sm:flex-nowrap items-center gap-3">
            <span className="text-xs font-bold text-gray-500 whitespace-nowrap uppercase tracking-wider">
              Filter by Crop:
            </span>
            <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 w-full">
              {farmerCrops.map((cropObj) => {
                const isActive = selectedCrop === cropObj.id
                return (
                  <button
                    key={cropObj.id}
                    onClick={() => setSelectedCrop(cropObj.id)}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap border ${
                      isActive
                        ? 'bg-emerald-700 text-white border-emerald-700 shadow-sm ring-2 ring-emerald-300'
                        : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-emerald-50 hover:text-emerald-800'
                    }`}
                  >
                    {cropObj.label}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Progress Bar */}
          {selectedCrop && selectedCrop !== 'All' && (
            <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-xs">
              <div className="flex justify-between text-xs font-semibold text-gray-600 mb-2.5">
                <span>🌱 Soil Prep & Sowing ({translateCrop ? translateCrop(selectedCrop) : selectedCrop})</span>
                <span className="text-emerald-700 font-bold">{completedTasksCount}/{displayTasks.length} Tasks Completed ({progressPercent}%)</span>
                <span>🏪 Market Sale & Settlement</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-emerald-600 to-teal-500 h-3 rounded-full transition-all duration-700"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Timeline */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader
                  title={t('workflow.seasonTimeline', 'Seasonal Crop Lifecycle Timeline')}
                  icon="📅"
                  subtitle={
                    activePlotForCrop && activePlotForCrop.sowing_date
                      ? `🌱 Sowing Date: ${activePlotForCrop.sowing_date} → 🌾 Target Harvest: ${activePlotForCrop.expected_harvest || 'N/A'} (${activePlotForCrop.crop_name || selectedCrop})`
                      : `Phases of crop growth & market execution (${selectedCrop === 'All' ? 'All Crops' : selectedCrop})`
                  }
                />
                <div className="pt-2">
                  {timelineSteps.map((step, idx) => (
                    <TimelineItem
                      key={step.id || idx}
                      step={step}
                      isLast={idx === timelineSteps.length - 1}
                    />
                  ))}
                </div>
              </Card>
            </div>

            {/* Real Tasks List */}
            <div>
              <Card>
                <CardHeader
                  title={t('workflow.allTasks', 'Crop Action Tasks')}
                  icon="✅"
                  subtitle={`${displayTasks.filter(t => t.status === 'Completed').length}/${displayTasks.length} ${selectedCrop === 'All' ? (activePlotForCrop?.crop_name || 'Crop') : selectedCrop} Tasks`}
                />
                <div className="space-y-2.5">
                  {loading ? (
                    <div className="py-8 text-center text-xs text-gray-400 animate-pulse">Loading tasks from database...</div>
                  ) : displayTasks.length === 0 ? (
                    <div className="p-6 text-center text-xs text-gray-500 bg-gray-50 rounded-xl border border-dashed">
                      No active tasks found for <b>{selectedCrop}</b>. Click <b>"Generate AI Lifecycle Workflow"</b> above or add a task manually!
                    </div>
                  ) : (
                    displayTasks.map((task) => (
                      <TaskCard key={task.id} task={task} onToggle={toggleTask} />
                    ))
                  )}
                </div>
              </Card>
            </div>
          </div>
        </div>

      {/* CREATE WORKFLOW TASK MODAL */}
      {showTaskModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleCreateTask} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">➕ Create Workflow Task</h3>
              <button type="button" onClick={() => setShowTaskModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-gray-700 block mb-1">Task Title *</label>
                <input
                  type="text"
                  value={newTask.title}
                  onChange={e => setNewTask({ ...newTask, title: e.target.value })}
                  placeholder="e.g. Apply NPK Fertilizer"
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-gray-700 block mb-1">Crop *</label>
                  <select
                    value={newTask.crop}
                    onChange={e => setNewTask({ ...newTask, crop: e.target.value })}
                    className="w-full px-3.5 py-2 border rounded-xl text-sm bg-white"
                  >
                    {farmerCrops.map(c => (
                      <option key={c.id} value={c.id}>{c.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-gray-700 block mb-1">Priority</label>
                  <select
                    value={newTask.priority}
                    onChange={e => setNewTask({ ...newTask, priority: e.target.value })}
                    className="w-full px-3 py-2 border rounded-xl text-sm"
                  >
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-gray-700 block mb-1">Due Date</label>
                <input
                  type="date"
                  value={newTask.due_date}
                  onChange={e => setNewTask({ ...newTask, due_date: e.target.value })}
                  className="w-full px-3.5 py-2 border rounded-xl text-sm"
                />
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowTaskModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">Cancel</button>
              <button type="submit" className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold cursor-pointer">Save Task →</button>
            </div>
          </form>
        </div>
      )}

      {/* ADVANCE DEAL WORKFLOW MODAL */}
      {showDealModal && selectedDeal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleAdvanceDealStatus} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">🔄 Advance Deal Contract Stage</h3>
              <button type="button" onClick={() => setShowDealModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-gray-700 block mb-1">Select New Deal Stage *</label>
                <select
                  value={dealNewStatus}
                  onChange={e => setDealNewStatus(e.target.value)}
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500 font-semibold"
                >
                  <option value="Harvest Scheduled">Harvest Scheduled</option>
                  <option value="Packaging">Packaging</option>
                  <option value="Transport & Pickup">Transport & Pickup</option>
                  <option value="Delivered">Delivered</option>
                  <option value="Payment Completed">Payment Completed (Auto-Syncs Ledger)</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>

              {dealNewStatus === 'Payment Completed' && (
                <div className="grid grid-cols-2 gap-3 bg-emerald-50 p-3 rounded-xl border border-emerald-200">
                  <div>
                    <label className="font-semibold text-gray-700 block mb-1">Transport Cost (₹)</label>
                    <input
                      type="number"
                      value={transportCost}
                      onChange={e => setTransportCost(e.target.value)}
                      className="w-full px-3 py-2 border rounded-xl text-sm"
                    />
                  </div>
                  <div>
                    <label className="font-semibold text-gray-700 block mb-1">Packaging Cost (₹)</label>
                    <input
                      type="number"
                      value={packagingCost}
                      onChange={e => setPackagingCost(e.target.value)}
                      className="w-full px-3 py-2 border rounded-xl text-sm"
                    />
                  </div>
                </div>
              )}
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowDealModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">Cancel</button>
              <button type="submit" disabled={updatingDeal} className="px-5 py-2 bg-blue-900 hover:bg-blue-950 text-white rounded-xl text-xs font-bold cursor-pointer disabled:opacity-50">
                {updatingDeal ? 'Updating...' : 'Update Deal Stage →'}
              </button>
            </div>
          </form>
        </div>
      )}

    </div>
  )
}

export default Workflow
