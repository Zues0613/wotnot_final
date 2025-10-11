<template>
  <!-- Main app container -->
  <div id="app" class="flex h-screen flex-col font-sans">

    <!-- Navbar -->
    <div
      class="navbar fixed top-0 left-0 right-0 z-30 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 dark:border-gray-700 dark:bg-gray-800">
      <div class="nav-left flex items-center">
        <!-- Hamburger Menu (Mobile) -->
        <button @click="isMenuOpen = !isMenuOpen"
          class="mr-3 p-2 text-gray-600 hover:text-green-700 dark:text-gray-300 md:hidden">
          <i class="bi bi-list text-2xl"></i>
        </button>

        <div class="logo-div">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
            <path fill="#166534"
              d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
          </svg>
        </div>
        <div class="logo"> WotNot</div>

        <!-- Desktop Navigation -->
        <div class="hidden items-center md:flex">
          <div class="nav-item" v-for="section in navItems" :key="section.name" @click="navigate(section.path)"
            :class="{ active: isActive(section.path) }">
            <i :class="section.icon"></i><span>{{ section.label }}</span>
          </div>
        </div>
      </div>

      <div class="nav-right flex items-center">
        <!-- Dark Mode Toggle -->
        <button @click="toggleDarkMode" class="p-2">
          <i v-if="isDarkMode" class="bi bi-moon-fill"></i>
          <i v-else class="bi bi-sun-fill"></i>
        </button>

        <div class="flex items-center" v-if="user">
          <p class="mr-2 hidden text-green-700 sm:block"> {{ user.email }}</p>
        </div>
        <div v-else>
          <p class="mr-2 text-gray-600">Session Expired</p>
        </div>

        <div class="profile-dropdown relative" @click="toggleDropdown" ref="profileDropdown">
          <div class="profile-icon">
            <div v-if="profile.profile_picture_url">
              <img :src="profile.profile_picture_url" alt="Profile Picture">
            </div>
            <div v-else>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-person-circle h-full w-full" viewBox="0 0 16 16">
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                <path fill-rule="evenodd"
                  d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1" />
              </svg>
            </div>
          </div>

          <div v-if="dropdownOpen" class="dropdown-menu" ref="dropdownMenu">
            <ul>
              <li @click="goToProfile"><i class="bi bi-person-circle"></i> View Profile</li>
              <li @click="goToCostAnalytics"><i class="bi bi-currency-rupee"></i> Purchase History </li>
              <li @click="goToSettings"><i class="bi bi-gear-fill"></i> Settings</li>
              <li @click="logout"><i class="bi bi-box-arrow-right"></i> Logout</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex flex-1 overflow-hidden pt-16">
      <!-- Sidebar -->
      <aside
        class="fixed top-16 left-0 z-20 h-[calc(100vh-4rem)] w-64 transform overflow-y-auto bg-gray-100 p-4 transition-transform duration-300 ease-in-out dark:bg-gray-900 md:translate-x-0"
        :class="{ '-translate-x-full': !isMenuOpen }">

        <!-- Broadcast Section Sidebar -->
        <div v-if="currentSection === 'broadcast'">
          <a href="#" @click.prevent="navigate('/broadcast/messages')"
            :class="{ 'text-green-800 font-semibold': isActive('/broadcast/messages'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/messages') }"
            class="block rounded-lg p-3 text-gray-600">
            <i class="bi bi-broadcast mr-2"></i>Broadcast Messages
          </a>
          <a href="#" @click.prevent="navigate('/broadcast/templates')"
            :class="{ 'text-green-800 font-semibold': isActive('/broadcast/templates'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/templates') }"
            class="block rounded-lg p-3 text-gray-600">
            <i class="bi bi-chat-right-text-fill mr-2"></i>Manage Templates
          </a>
          <a href="#" @click.prevent="navigate('/broadcast/scheduled')"
            :class="{ 'text-green-800 font-semibold': isActive('/broadcast/scheduled'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/scheduled') }"
            class="block rounded-lg p-3 text-gray-600">
            <i class="bi bi-calendar2-range-fill mr-2"></i>Scheduled Broadcasts
          </a>
        </div>

        <!-- Contacts Section Sidebar -->
        <div v-if="currentSection === 'Contacts'">
          <a href="#" @click.prevent="navigate('/contacts/list')"
            :class="{ 'text-green-800 font-semibold': isActive('/contacts/list'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/contacts/list') }"
            class="block rounded-lg p-3 text-gray-600">
            <i class="bi bi-journal-bookmark-fill mr-2 "></i>Manage Contacts
          </a>
          <a href="#" @click.prevent="navigate('/contacts/groups')"
            :class="{ 'text-green-800 font-semibold': isActive('/contacts/groups'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/contacts/groups') }"
            class="block rounded-lg p-3 text-gray-600">
            <i class="bi bi-tags-fill mr-2"></i>Manage Tags
          </a>
        </div>

        <!-- Integration Section Sidebar -->
        <div v-if="currentSection === 'Integration'">
          <a href="#" @click.prevent="navigate('/integration/woocommerce')"
            :class="{ 'text-green-800 font-semibold': isActive('/integration/woocommerce'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/integration/woocommerce') }"
            class="block rounded-lg p-3 text-gray-600"><i class="bi bi-link-45deg"></i>
            Woocommerce
          </a>
        </div>

        <!-- Analytics Section Sidebar -->
        <div v-if="currentSection === 'Analytics'">
          <a href="#" @click.prevent="navigate('/analytics/cost')"
            :class="{ 'text-green-800 font-semibold': isActive('/analytics/cost'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/analytics/cost') }"
            class="block rounded-lg p-3 text-gray-600"><i class="bi bi-currency-dollar"></i>
            Cost
          </a>
          <a href="#" @click.prevent="navigate('/analytics/conversations')"
            :class="{ 'text-green-800 font-semibold': isActive('/analytics/conversations'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/analytics/conversations') }"
            class="block rounded-lg p-3 text-gray-600"><i class="bi bi-link-45deg"></i>
            Conversations
          </a>
        </div>
      </aside>

      <!-- Router View / Main content -->
      <main class="flex-1 overflow-y-auto bg-white p-6 dark:bg-gray-950 md:ml-64">
        <router-view></router-view>
      </main>

    </div>


    <!-- Wallet Modal Pop-up -->
    <div v-if="walletModalOpen" class="modal-overlay">
      <div class="modal-content w-11/12 max-w-md" @click.stop>
        <div class="modal-header">
          <h2>Wallet</h2>
          <span class="close-btn" @click="toggleWalletModal">&times;</span>
        </div>
        <p><strong>Current Balance:</strong> {{ currentBalance }}</p>
        <button @click="topUpBalance" class="topup-btn">Top Up Balance</button>
      </div>
    </div>

    <!-- Profile Popup -->
    <ProfilePopup :visible="showProfilePopup" :user="user" @close="showProfilePopup = false" />
  </div>
</template>

<script>

/* global FB */
import { useRouter, useRoute } from 'vue-router';
import ProfilePopup from './profile.vue';
import axios from "axios";

export default {
  name: 'DashboardView',
  components: {
    ProfilePopup
  },
  data() {
    return {
      isDarkMode: false,
      apiUrl: process.env.VUE_APP_API_URL,
      localUser: {
        whatsapp_business_id: '',
      },
      navItems: [
        { name: 'broadcast', label: 'Broadcast', icon: 'bi bi-broadcast', path: '/broadcast/messages' },
        { name: 'Contacts', label: 'Contacts', icon: 'bi bi-person-video2', path: '/contacts/list' },
        { name: 'Integration', label: 'Integration', icon: 'bi bi-plugin', path: '/integration/woocommerce' },
        { name: 'chatbot', label: 'Chatbot', path: '/chatbot', icon: 'bi bi-robot' },
        { name: 'Analytics', label: 'Analytics', path: '/analytics/cost', icon: 'bi bi-graph-up' },
      ],
      user: null,
      dropdownOpen: false,
      showProfilePopup: false,
      isMenuOpen: false,
      walletModalOpen: false,
      currentBalance: 0,
      profile: {
        about: "",
        address: "",
        email: "",
        description: "",
        websites: "",
        vertical: "OTHER",
        messaging_product: "whatsapp",
        profile_picture_url: ""
      },
      originalProfile: {},
    }
  },
  setup() {
    const router = useRouter();
    const route = useRoute();

    const isActive = (path) => route.path.startsWith(path.split('/')[1]); // Check root path
    const navigate = (path) => {
      router.push(path);
    }

    return {
      navigate,
      isActive,
      currentSection: getSectionFromRoute(route.path),
    };
  },
  watch: {
    '$route.path': function (newPath) {
      this.currentSection = getSectionFromRoute(newPath);
      this.isMenuOpen = false; // Close mobile menu on navigation
    }
  },
  async mounted() {
    if (localStorage.getItem('darkMode') === 'true') {
      this.isDarkMode = true;
      document.documentElement.classList.add('dark');
    }
    await this.fetchProfile();
    await this.fetchUserDetails();
    await this.created();
    document.addEventListener('click', this.handleOutsideClick);


    const checkAndSend = () => {
      if (this.sessionInfoResponse && this.sdkResponse) {
        // Send data to the backend
        fetch(`${this.apiUrl}/subscribe_customer`, {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sessionInfoResponse: this.sessionInfoResponse,
            sdkResponse: this.sdkResponse,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Response from backend:", data);
          })
          .catch((error) => {
            console.error("Error sending data to backend:", error);
          });
      }
    };

    this.$watch(
      () => [this.sessionInfoResponse, this.sdkResponse],
      (newValues) => {
        const [newSessionInfoResponse, newSdkResponse] = newValues;
        if (newSessionInfoResponse && newSdkResponse) {
          checkAndSend();
        }
      },
      { immediate: true, deep: true }
    );

    window.fbAsyncInit = () => {
      FB.init({
        appId: "2621821927998797",
        autoLogAppEvents: true,
        xfbml: true,
        version: "v21.0",
      });
    };

    const script = document.createElement("script");
    script.src = "https://connect.facebook.net/en_US/sdk.js";
    script.async = true;
    script.defer = true;
    script.crossOrigin = "anonymous";
    document.body.appendChild(script);

    window.addEventListener("message", (event) => {
      if (
        event.origin !== "https://www.facebook.com" &&
        event.origin !== "https://web.facebook.com"
      ) {
        return;
      }

      try {
        const data = JSON.parse(event.data);
        if (data.type === "WA_EMBEDDED_SIGNUP") {
          if (data.event === "FINISH") {
            const { phone_number_id, waba_id } = data.data;
            console.log(
              "Phone number ID:",
              phone_number_id,
              "WhatsApp business account ID:",
              waba_id
            );
          } else if (data.event === "CANCEL") {
            const { current_step } = data.data;
            console.warn("Cancelled at step:", current_step);
          } else if (data.event === "ERROR") {
            const { error_message } = data.data;
            console.error("Error:", error_message);
          }
        }
        this.sessionInfoResponse = JSON.stringify(data, null, 2);

      } catch {
        console.log("Non-JSON Response:", event.data);
      }
    });
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick);
  },

  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('darkMode', 'true');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('darkMode', 'false');
      }
    },

    async created() {
      try {
        const response = await fetch(`${this.apiUrl}/user`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        this.user = await response.json();
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },

    async fetchUserDetails() {
      try {
        const response = await fetch(`${this.apiUrl}/user`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        const data = await response.json();
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];

      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },

    async fetchWalletDetails(accountId) {
      try {

        const response = await fetch(`${this.apiUrl}/conversations-cost/${accountId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const costData = await response.json();

        this.currentBalance = costData;
        this.currentBalance = this.currentBalance.toFixed(3);


      } catch (error) {
        console.error('Error fetching wallet details:', error);
        return null;
      }
    },

    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.warn('No token found, skipping profile fetch');
          return;
        }

        const response = await axios.get(`${this.apiUrl}/get-business-profile/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status >= 200 && response.status < 300 && response.data.data.length) {
          const data = response.data.data[0];
          this.profile = {
            about: data.about || "",
            address: data.address || "",
            email: data.email || "",
            websites: (data.websites && data.websites.join(", ")) || "",
            vertical: data.vertical || "OTHER",
            messaging_product: data.messaging_product || "whatsapp",
            description: data.description || "",
            profile_picture_url: data.profile_picture_url || "",
          };
          this.originalProfile = { ...this.profile };
        }
      } catch (error) {
        // Handle errors gracefully - WhatsApp Business Account may not be configured yet
        if (error.response?.status === 401) {
          console.warn('Unauthorized - WhatsApp Business Account credentials not configured');
        } else if (error.response?.status === 404 || error.response?.status === 400) {
          console.warn('WhatsApp Business Profile not available');
        } else {
          console.error("Error fetching profile:", error.response?.data?.detail || error.message);
        }
        // Don't show error to user - this is expected for new users
      } finally {
        this.loading = false;
      }
    },

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async toggleWalletModal() {
      this.walletModalOpen = !this.walletModalOpen;
      const walletOpen = this.walletModalOpen

      if (walletOpen) {
        await this.fetchWalletDetails(this.localUser.whatsapp_business_id)
      }
    },
    topUpBalance() {
      alert('Coming Soon...');
    },
    goToProfile() {
      this.showProfilePopup = true;
    },
    goToSettings() {
      this.$router.push('/settings');
    },
    goToCostAnalytics() {
      this.$router.push('/analytics/cost');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },

    handleOutsideClick(event) {
      const dropdownMenu = this.$refs.dropdownMenu;
      const profileDropdown = this.$refs.profileDropdown;

      if (dropdownMenu && !dropdownMenu.contains(event.target) && profileDropdown && !profileDropdown.contains(event.target)) {
        this.dropdownOpen = false;
      }
    },

  }
}

function getSectionFromRoute(path) {
  if (path.startsWith('/broadcast')) return 'broadcast';
  if (path.startsWith('/contacts')) return 'Contacts';
  if (path.startsWith('/integration')) return 'Integration';
  if (path.startsWith('/chatbot')) return 'Chatbot';
  if (path.startsWith('/analytics')) return 'Analytics';
  if (path.startsWith('/agent')) return 'AIagent';
  return 'broadcast'; // Default section
}
</script>

<style>
.dark body {
  background-color: #1a202c;
  color: #a0aec0;
}

.dark .navbar {
  background-color: #2d3748;
}

.dark .logo {
  color: #48bb78;
}

.dark .nav-item {
  color: #a0aec0;
}

.dark .nav-item:hover {
  color: #48bb78;
}

.dark .profile-icon {
  background-color: #4a5568;
  border-color: #718096;
}

.dark .dropdown-menu {
  background-color: #2d3748;
  color: #a0aec0;
}

.dark .dropdown-menu li:hover {
  background-color: #4a5568;
}

.dark .bg-gray-100 {
  background-color: #2d3748;
}

.dark .text-gray-600 {
  color: #a0aec0;
}

.dark .text-green-800 {
  color: #48bb78;
}

.dark .hover\:bg-gray-200:hover {
  background-color: #4a5568;
}

.dark .bg-white {
  background-color: #1a202c;
}

.dark .bg-gray-950 {
    background-color: #111827; /* A slightly different dark for the main content */
}


.Toastify__toast-container {
  z-index: 11000 !important;
}

/* Base body styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
}

.logo {
  font-weight: 800;
  margin: 8px 0;
  padding-right: 30px;
  font-size: xx-large;
  color: #166534;
}

.logo-div svg {
  width: 62px;
  height: 62px;
  padding: 15px 10px 10px 10px;
  color: #075e54;
}

.nav-right svg {
  width: 36px;
  height: 36px;
  padding: 0;
  margin: 0 9px 0 9px;
  color: #525252;
  transition: all 0.3s ease;
}

.nav-right svg:hover {
  border-radius: 100%;
  transform: translateY(-3px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.nav-item {
  padding: 15px;
  cursor: pointer;
  color: #525252;
  text-align: center;
  margin: 8px 0;
  border-right: 1px solid #e9ecef;
  font-size: medium;
}

.profile-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #ddd;
  border: 1px solid grey;
  cursor: pointer;
}

.profile-icon img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.dropdown-menu {
  position: absolute;
  top: 60px; /* Adjusted for new navbar height */
  right: 0;
  width: 200px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  color: #525252;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  padding: 10px;
  cursor: pointer;
  font-size: 18px;
}

.dropdown-menu li:hover {
  background-color: #f1f1f1;
}

.dropdown-menu li i {
  margin-right: 9px;
}

.nav-item i {
  padding-right: 9px;
}

.nav-item:hover {
  font-weight: 600;
  border-radius: 5px;
  color: #075e54;
}

button {
  background-color: #075e54;
  color: white;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1ebd5b;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  text-align: center;
  position: relative;
  animation: fadeIn 0.3s ease;
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Close Button (X) */
.close-btn {
  position: absolute;
  right: 15px;
  top: 15px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  color: #333;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #ff0000;
}

/* Top-Up Button */
.topup-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 30px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.topup-btn:hover {
  background-color: #218838;
}

/* Fade-in Animation for Modal */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
