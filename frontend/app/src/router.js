import { createRouter, createWebHistory } from "vue-router";
import BroadCast1 from "./components/broadcast/broadcast1.vue";
import BroadCast2 from "./components/broadcast/broadcast2.vue";
import BroadCast3 from "./components/broadcast/broadcast3.vue";
import ContActs1 from "./components/contacts/contacts1.vue";
import ContActs2 from "./components/contacts/contacts2.vue";
import AppIntegration from "./components/integration/integration.vue";
import LoginPage from "./components/login/login.vue";
import AIagent from "./components/AIagent/AIagent.vue";
import BasicSignupPage from "./components/signup/basic_signup.vue";
import DashboardView from "./views/dashboardview.vue";
import Profile from "./views/profile.vue";
import Settings from "./views/profileSettings.vue";
import ChatbotView from "./components/chatbot/chatbotview.vue"; // Ensure this path is correct
import CostAnalytics from "./components/PurchaseHistory/CostDashboard.vue";
import Analytics from "./components/analytics/Analytics.vue";

import TermsAndPrivacy from "./views/TermsAndPrivacy.vue";
import TermsOfService from "./views/TermsOfService.vue";
import PrivacyPolicy from "./views/PrivacyPolicy.vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const routes = [
  // Public routes
  { path: "/", component: LoginPage, name: "Login" },
  { path: "/signup", component: BasicSignupPage, name: "Signup" },

  {
    path: "/terms-and-privacy",
    component: TermsAndPrivacy,
    name: "TermsAndPrivacy",
  },
  {
    path: "/terms-of-service",
    component: TermsOfService,
    name: "TermsOfService",
  },
  {
    path: "/privacy-policy",
    component: PrivacyPolicy,
    name: "PrivacyPolicy",
  },

  // Protected routes within the dashboard
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
    children: [
      // AI Agent
      { path: "/agent", component: AIagent, name: "AIagent" },
      
      // Analytics
      {
        path: "/analytics/cost",
        component: CostAnalytics,
        name: "CostAnalytics",
      },
      {
        path: "/analytics/conversations",
        component: Analytics,
        name: "DataAnalytics",
      },
      
      // Broadcast Routes (Clean URLs)
      {
        path: "/broadcast/templates",
        component: BroadCast1,
        name: "Templates",
      },
      {
        path: "/broadcast/messages",
        component: BroadCast2,
        name: "BroadcastMessages",
      },
      {
        path: "/broadcast/scheduled",
        component: BroadCast3,
        name: "ScheduledBroadcasts",
      },
      
      // Contacts Routes (Clean URLs)
      { 
        path: "/contacts/list", 
        component: ContActs1, 
        name: "ContactsList" 
      },
      { 
        path: "/contacts/groups", 
        component: ContActs2, 
        name: "ContactsGroups" 
      },
      
      // Integration
      {
        path: "/integration/woocommerce",
        component: AppIntegration,
        name: "WooCommerceIntegration",
      },
      
      // Chatbot
      {
        path: "/chatbot",
        component: ChatbotView,
        name: "Chatbot",
      },
      
      // Profile & Settings
      { path: "/profile", component: Profile, name: "Profile" },
      { path: "/settings", component: Settings, name: "Settings" },
      
      // Default redirect when accessing /dashboard
      { path: "", redirect: "/broadcast/messages" },
      
      // Backward compatibility redirects (old URLs → new URLs)
      { path: "/broadcast/broadcast1", redirect: "/broadcast/templates" },
      { path: "/broadcast/broadcast2", redirect: "/broadcast/messages" },
      { path: "/broadcast/broadcast3", redirect: "/broadcast/scheduled" },
      { path: "/contacts/contacts1", redirect: "/contacts/list" },
      { path: "/contacts/contacts2", redirect: "/contacts/groups" },
      { path: "/integration/integration1", redirect: "/integration/woocommerce" },
      { path: "/chatbot/chatbotview", redirect: "/chatbot" },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for authentication and token expiration
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  // If user is logged in and trying to access login/signup page, redirect to dashboard
  if (token && (to.path === "/" || to.path === "/signup")) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const now = Math.floor(Date.now() / 1000);

      // If token is valid, redirect to dashboard
      if (payload.exp >= now) {
        return next("/dashboard");
      }
    } catch (error) {
      // Invalid token, allow access to login
      localStorage.removeItem("token");
    }
  }

  // Check if route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // No token = not logged in
      toast.error("Session expired. Please log in again.");
      return next("/");
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp < now) {
        // Token expired
        localStorage.removeItem("token");
        toast.error("Session expired. Please log in again.");
        return next("/");
      }
    } catch (error) {
      // Invalid token format or parsing error
      localStorage.removeItem("token");
      toast.error("Invalid session. Please log in again.");
      return next("/");
    }
  }

  // If route doesn't require auth or token is valid
  next();
});


export default router;
