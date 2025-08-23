import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const endpoints = {
  // Auth endpoints
  auth: { 
    login: '/users/login', 
    register: '/users/register', 
    me: '/users/me',
    update: '/users/me'
  },
  
  // User Management endpoints
  users: {
    // Basic user operations
    list: '/users/',
    get: (id: number) => `/users/${id}`,
    create: '/users/',
    update: (id: number) => `/users/${id}`,
    deactivate: (id: number) => `/users/${id}/deactivate`,
    activate: (id: number) => `/users/${id}/activate`,
    
    // User specific operations
    getRole: '/users/me/role',
    changeRole: (id: number) => `/users/${id}/role`,
    resetPassword: (id: number) => `/users/${id}/reset-password`,
    validateNationalId: '/users/validate-national-id',
    
    // Government officers
    getOfficers: '/users/officers',
    
    // Search and statistics
    search: (term: string) => `/users/search/${term}`,
    getStatistics: '/users/statistics/dashboard'
  },
  
  // Department endpoints
  departments: { 
    // Basic CRUD
    list: '/departments/', 
    get: (id: number) => `/departments/${id}`,
    create: '/departments/',
    update: (id: number) => `/departments/${id}`,
    activate: (id: number) => `/departments/${id}/activate`,
    deactivate: (id: number) => `/departments/${id}/deactivate`,
    
    // Related data
    services: (id: number) => `/departments/${id}/services`,
    officers: (id: number) => `/departments/${id}/officers`,
    
    // Search and filtering
    search: (term: string) => `/departments/search/${term}`,
    byLocation: (location: string) => `/departments/location/${location}`,
    byOperatingHours: (day: string) => `/departments/operating-hours/${day}`,
    
    // Statistics
    getStatistics: (id: number) => `/departments/${id}/statistics`,
    getAllStatistics: '/departments/statistics/overview',
    getWithPagination: '/departments/pagination/list'
  },
  
  // Service endpoints
  services: { 
    // Basic CRUD
    list: '/services/', 
    get: (id: number) => `/services/${id}`,
    create: '/services/',
    update: (id: number) => `/services/${id}`,
    activate: (id: number) => `/services/${id}/activate`,
    deactivate: (id: number) => `/services/${id}/deactivate`,
    
    // Related data
    byDepartment: (id: number) => `/services/department/${id}`,
    
    // Search and filtering
    search: '/services/search',
    byDuration: '/services/duration/range',
    byDocuments: (type: string) => `/services/documents/${type}`,
    
    // Statistics and analytics
    getStatistics: (id: number) => `/services/${id}/statistics`,
    getPopular: '/services/popular/top-rated',
    getCapacityUtilization: (id: number) => `/services/${id}/capacity-utilization`,
    getWithPagination: '/services/pagination/list'
  },
  
  // Appointment endpoints
  appointments: {
    // Basic CRUD
    mine: '/appointments/me', 
    create: '/appointments/',
    get: (id: number) => `/appointments/${id}`,
    update: (id: number) => `/appointments/${id}`,
    cancel: (id: number) => `/appointments/${id}/cancel`,
    
    // Appointment operations
    reschedule: (id: number) => `/appointments/${id}/reschedule`,
    updateStatus: (id: number) => `/appointments/${id}/status`,
    getQrCode: (id: number) => `/appointments/${id}/qr-code`,
    
    // Search and filtering
    byReference: (ref: string) => `/appointments/reference/${ref}`,
    byService: (id: number) => `/appointments/service/${id}`,
    byDepartment: (id: number) => `/appointments/department/${id}`,
    search: '/appointments/search',
    
    // Analytics
    getStatistics: '/appointments/analytics/statistics',
    
    // Time slots
    timeSlotsAvailable: (sid: number) => `/appointments/time-slots/${sid}/available`,
    timeSlotsCreate: '/appointments/time-slots/',
    timeSlotsCreateSingle: '/appointments/time-slots/single',
    timeSlotsCreateRecurring: '/appointments/time-slots/recurring'
  },
  
  // Document endpoints
  documents: { 
    // Basic CRUD
    upload: '/documents/upload', 
    mine: '/documents/me',
    get: (id: number) => `/documents/${id}`,
    update: (id: number) => `/documents/${id}`,
    delete: (id: number) => `/documents/${id}`,
    
    // Document operations
    verify: (id: number) => `/documents/${id}/verify`,
    reject: (id: number) => `/documents/${id}/reject`,
    download: (id: number) => `/documents/download/${id}`,
    
    // Related data
    byAppointment: (id: number) => `/documents/appointment/${id}`,
    byType: (type: string) => `/documents/type/${type}`,
    
    // Search and filtering
    searchMine: '/documents/search/me',
    needingVerification: '/documents/needing-verification',
    
    // Statistics and validation
    getStatistics: '/documents/statistics/overview',
    getRequiredTypes: (serviceId: number) => `/documents/types/required/${serviceId}`,
    validateRequirements: (appointmentId: number) => `/documents/validation/${appointmentId}`
  },
  
  // Notification endpoints
  notifications: { 
    // Basic CRUD
    mine: '/notifications/me', 
    create: '/notifications/',
    get: (id: number) => `/notifications/${id}`,
    delete: (id: number) => `/notifications/${id}`,
    
    // Notification operations
    markRead: (id: number) => `/notifications/${id}/read`,
    markAllRead: '/notifications/me/read-all',
    getUnreadCount: '/notifications/unread/count',
    
    // Specific notification types
    appointmentConfirmation: (id: number) => `/notifications/appointment/${id}/confirmation`,
    appointmentReminder: (id: number) => `/notifications/appointment/${id}/reminder`,
    statusUpdate: (id: number) => `/notifications/appointment/${id}/status-update`,
    documentRequest: (userId: number) => `/notifications/user/${userId}/document-request`,
    
    // Scheduling and management
    scheduleReminders: '/notifications/schedule-reminders',
    cleanupOld: '/notifications/cleanup/old',
    
    // Search and filtering
    byType: (type: string) => `/notifications/type/${type}`,
    getStatistics: '/notifications/statistics/overview'
  },
  
  // Feedback endpoints
  feedback: { 
    // Basic CRUD
    create: '/feedback', 
    mine: '/feedback/me',
    get: (id: number) => `/feedback/${id}`,
    update: (id: number) => `/feedback/${id}`,
    delete: (id: number) => `/feedback/${id}`,
    
    // Related data
    byAppointment: (id: number) => `/feedback/appointment/${id}`,
    byService: (id: number) => `/feedback/service/${id}`,
    byDepartment: (id: number) => `/feedback/department/${id}`,
    
    // Statistics and analytics
    getServiceStatistics: (id: number) => `/feedback/statistics/service/${id}`,
    getDepartmentStatistics: (id: number) => `/feedback/statistics/department/${id}`,
    getOverallStatistics: '/feedback/statistics/overview',
    getTopRated: '/feedback/popular/top-rated',
    getTrends: '/feedback/trends/analysis',
    
    // Search and filtering
    advancedSearch: '/feedback/search/advanced',
    getRecent: '/feedback/recent/submissions',
    getSummary: '/feedback/summary/comprehensive'
  },
  
  // Analytics endpoints
  analytics: { 
    // Dashboard and overview
    dashboardOverview: '/analytics/dashboard/overview',
    
    // Specific analytics
    appointmentTrends: '/analytics/appointments/trends',
    departmentPerformance: '/analytics/departments/performance',
    userEngagement: '/analytics/users/engagement',
    capacityUtilization: '/analytics/capacity/utilization',
    documentOverview: '/analytics/documents/overview',
    feedbackSatisfaction: '/analytics/feedback/satisfaction'
  },
  
  // System endpoints
  system: {
    root: '/',
    health: '/health',
    info: '/api/v1/info'
  }
}

// Helper function to handle API errors
export const handleApiError = (error: any) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.detail || error.response.data?.message || 'An error occurred'
    return { message, status: error.response.status }
  } else if (error.request) {
    // Request made but no response
    return { message: 'No response from server. Please check your connection.', status: 0 }
  } else {
    // Something else happened
    return { message: error.message || 'An unexpected error occurred', status: 0 }
  }
}

// Helper function to format API responses
export const formatApiResponse = (response: any) => {
  return {
    data: response.data,
    status: response.status,
    success: response.status >= 200 && response.status < 300
  }
}


