import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Departments from '../views/Departments.vue'
import Services from '../views/Services.vue'
import Book from '../views/Book.vue'
import DashboardLanding from '../views/Dashboard.vue'
import DashboardAdmin from '../views/dashboards/Admin.vue'
import DashboardOfficer from '../views/dashboards/Officer.vue'
import DashboardUser from '../views/dashboards/User.vue'
import AdminDepartments from '../views/admin/AdminDepartments.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'
import AdminServices from '../views/admin/AdminServices.vue'
import AdminTimeSlots from '../views/admin/AdminTimeSlots.vue'
import AdminAnalytics from '../views/admin/AdminAnalytics.vue'
import OfficerAppointments from '../views/officer/OfficerAppointments.vue'
import OfficerDocuments from '../views/officer/OfficerDocuments.vue'
import MyAppointments from '../views/user/MyAppointments.vue'
import MyDocuments from '../views/user/MyDocuments.vue'
import MyNotifications from '../views/user/MyNotifications.vue'
import Feedback from '../views/user/Feedback.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/departments', component: Departments },
    { path: '/services', component: Services },
    { path: '/book', component: Book, meta: { requiresAuth: true, role: 'citizen' } },
    { path: '/dashboard', component: DashboardLanding, meta: { requiresAuth: true } },
    {
      path: '/dashboard/admin', component: DashboardAdmin, meta: { requiresAuth: true, role: 'admin' },
      children: [
        { path: 'departments', component: AdminDepartments },
        { path: 'users', component: AdminUsers },
        { path: 'services', component: AdminServices },
        { path: 'time-slots', component: AdminTimeSlots },
        { path: 'analytics', component: AdminAnalytics },
      ]
    },
    {
      path: '/dashboard/officer', component: DashboardOfficer, meta: { requiresAuth: true, role: 'government_officer' },
      children: [
        { path: 'appointments', component: OfficerAppointments },
        { path: 'documents', component: OfficerDocuments },
      ]
    },
    {
      path: '/dashboard/user', component: DashboardUser, meta: { requiresAuth: true, role: 'citizen' },
      children: [
        { path: 'appointments', component: MyAppointments },
        { path: 'documents', component: MyDocuments },
        { path: 'notifications', component: MyNotifications },
        { path: 'feedback', component: Feedback },
      ]
    },
  ]
})

router.beforeEach(async (to, _from, next) => {
    const auth = useAuthStore();
  
    // Hydrate user if we have a token but no user yet
    if (!auth.user && auth.token) {
      try { await auth.me(); } catch { /* ignore */ }
    }
  
    // Require auth
    if (to.meta.requiresAuth && !auth.user) {
      if (to.path !== '/login') return next({ path: '/login', replace: true });
      return next();
    }
  
    // Role-based target for dashboards
    const roleToDashboard = (role?: string) => {
      const r = (role || '').toLowerCase()
      if (r === 'admin') return '/dashboard/admin'
      if (r === 'government_officer') return '/dashboard/officer'
      return '/dashboard/user'
    }
  
    // Auto-redirect generic dashboard once
    if (to.path === '/dashboard' && auth.user) {
      const target = roleToDashboard(auth.user.role)
      return next({ path: target, replace: true })
    }
  
    // Enforce role on guarded routes
    if (to.meta.role && auth.user) {
      const userRole = (auth.user.role || '').toLowerCase()
      const requiredRole = String(to.meta.role).toLowerCase()
      const allowed = userRole === requiredRole || userRole === 'admin'
      if (!allowed) {
        const fallback = roleToDashboard(auth.user.role);
        if (to.path !== fallback) return next({ path: fallback, replace: true });
      }
    }
  
    return next();
  });
export default router


