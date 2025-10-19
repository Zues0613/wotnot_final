<template>
  <div class="bg-container">
    <!-- Success Animation Overlay -->
    <div v-if="showSuccessAnimation" class="success-overlay">
      <div class="success-animation">
        <div class="success-icon">
          <svg class="checkmark" viewBox="0 0 52 52">
            <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
            <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
          </svg>
        </div>
        <h2 class="success-title">Account Created Successfully!</h2>
        <p class="success-message">Logging you in automatically...</p>
        <div class="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <div class="max-w-md w-full bg-white p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center text-gray-800 mb-4">Get started with Wotnot</h2>




      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700">Business Name</label>
          <input type="text" id="username" placeholder="Your Business Name"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700">Business Email Address</label>
          <input type="email" id="email" placeholder="Your Business Email Address"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" placeholder="Set Password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="WABAID" class="block text-sm font-medium text-gray-700">WhatsApp Business Account ID</label>
          <input type="text" id="WABAID" placeholder="Your WhatsApp Business Account ID"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="PAccessToken" class="block text-sm font-medium text-gray-700">Permanent Access Token</label>
          <input type="text" id="PAccessToken" placeholder="Your Permanent Access Token"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="Phone_id" class="block text-sm font-medium text-gray-700">Phone Number ID</label>
          <input type="text" id="Phone_id" placeholder="Your Phone Number ID"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>
      </div>

      <div class="mt-4 text-sm text-center">
        <p class="mb-2 text-sm">
          By signing up you agree to the
          <router-link to="/terms-of-service" class="text-[#075e54] font-semibold hover:underline">Terms of Service</router-link> and
          <router-link to="/privacy-policy" class="text-[#075e54] font-semibold hover:underline">Privacy Policy</router-link>
        </p>
      </div>

      <button
        class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium flex items-center justify-center transition-all duration-300"
        @click.prevent="handleSubmit"
        :disabled="isLoading">
        <span v-if="!isLoading">Get Account</span>
        <div v-else class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          Creating Account...
        </div>
      </button>

      <p class="mt-4 text-center text-sm">
        Already have an account?
        <a href="" class="text-[#075e54] font-semibold mb-4" @click="redirectLogin">Login</a>
      </p>
    </div>
  </div>
</template>



<script>
/* global FB */
import { useToast } from 'vue-toastification';

export default {

  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      isLoading: false,
      showSuccessAnimation: false,
      sessionInfoResponse: "",
      sdkResponse: "",
    };
  },

  mounted() {
    // Initialize the Facebook SDK
    window.fbAsyncInit = () => {
      FB.init({
        appId: process.env.VUE_APP_FACEBOOK_APP_ID || "2621821927998797", // From environment variable
        autoLogAppEvents: true,
        xfbml: true,
        version: "v21.0",
      });
    };

    // Dynamically load the Facebook SDK
    const script = document.createElement("script");
    script.src = "https://connect.facebook.net/en_US/sdk.js";
    script.async = true;
    script.defer = true;
    script.crossOrigin = "anonymous";
    document.body.appendChild(script);

    // Set up an event listener for messages from Facebook
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
  name: 'SignUpForm',
  methods: {


    fbLoginCallback(response) {
      if (response.authResponse) {
        const code = response.authResponse.code;
        console.log("Auth Response Code:", code);
        // Handle the code by sending it to your backend server for further processing.
      }
      this.sdkResponse = JSON.stringify(response, null, 2);
    },

    launchWhatsAppSignup() {
      FB.login(
        this.fbLoginCallback,
        {
          config_id: process.env.VUE_APP_FACEBOOK_CONFIG_ID || "951833230236631", // From environment variable
          response_type: "code", // Must be 'code' for System User access token
          override_default_response_type: true,
          extras: {
            setup: {},
            featureType: "",
            sessionInfoVersion: "2",
          },
        }
      );
    },

    loadFacebookSDK() {
      if (!document.getElementById('facebook-jssdk')) {
        const script = document.createElement('script');
        script.id = 'facebook-jssdk';
        script.src = "https://connect.facebook.net/en_US/sdk.js";
        script.async = true;
        script.defer = true;
        script.onload = this.initializeFacebookSDK; // Ensure SDK is initialized once loaded
        document.body.appendChild(script);
      } else {
        this.initializeFacebookSDK(); // SDK is already loaded
      }
    },

    initializeFacebookSDK() {
      window.fbAsyncInit = () => {
        FB.init({
          appId: process.env.VUE_APP_FACEBOOK_APP_ID || '2621821927998797',  // From environment variable
          cookie: true,
          xfbml: true,
          version: 'v20.0',
        });
        this.renderFacebookButton();
      };
    },

    loginWithFacebook() {
      // Ensure the FB object is available
      if (window.FB) {
        window.FB.login(response => {
          if (response.authResponse) {
            console.log('User logged in:', response.authResponse);
            this.fetchUserDetails();
          } else {
            console.log('User cancelled login or did not fully authorize.');
          }
        }, { scope: 'email' });
      } else {
        console.error('Facebook SDK not loaded.');
      }
    },

    renderFacebookButton() {
      // Render the button manually after the SDK has loaded
      FB.XFBML.parse(document.getElementById('fb-login-btn'));
      console.log("run")
    },

    checkLoginState() {
      FB.getLoginStatus((response) => {
        if (response.status === 'connected') {
          // User is logged in and authenticated
          console.log('User is logged in and authenticated:', response);
          this.getUserInfo(); // Call a method to fetch user info
        } else if (response.status === 'not_authorized') {
          // User is logged into Facebook but has not authenticated your app
          console.log('User is logged into Facebook but not authenticated your app.');
        } else {
          // User is not logged into Facebook
          console.log('User is not logged into Facebook.');
        }
      });
    },
    fetchUserDetails() {
      window.FB.api('/me', { fields: 'id,name,email' }, userDetails => {
        console.log('User details:', userDetails);
      });
    },

    async handleSubmit() {
      const toast = useToast();
      this.isLoading = true;

      try {
        // Get the form data
        const formData = {
          username: document.getElementById('username').value,
          email: document.getElementById('email').value,
          password: document.getElementById('password').value,
          WABAID: document.getElementById('WABAID').value,
          PAccessToken: document.getElementById('PAccessToken').value,
          Phone_id: document.getElementById('Phone_id').value,
        };

        // Check for required fields
        if (!formData.username || !formData.email || !formData.password || !formData.WABAID || !formData.PAccessToken || !formData.Phone_id) {
          toast.error('Please fill in all required fields.');
          return;
        }

        // Send a request to your FastAPI endpoint
        const response = await fetch(`${this.apiUrl}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (data.success) {
          // Show success animation
          this.showSuccessAnimation = true;
          
          // Wait for animation to complete, then auto-login
          setTimeout(async () => {
            await this.autoLogin(formData.email, formData.password);
          }, 2000);
          
        } else if (data.detail) {
          toast.error(data.detail);
        } else {
          toast.error('Failed to create account. Please try again.');
        }
      } catch (error) {
        console.error('Error:', error);
        toast.error('Network error. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },

    async autoLogin(email, password) {
      const toast = useToast();
      
      try {
        // Auto-login after successful signup
        const loginResponse = await fetch(`${this.apiUrl}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: email,
            password: password
          })
        });

        const loginData = await loginResponse.json();

        if (loginData.access_token) {
          localStorage.setItem('token', loginData.access_token);
          toast.success('Welcome to WotNot! You are now logged in.');
          
          // Redirect to dashboard
          setTimeout(() => {
            this.$router.push('/dashboard');
          }, 1000);
        } else {
          // If auto-login fails, redirect to login page
          toast.info('Account created successfully! Please log in.');
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Auto-login error:', error);
        // If auto-login fails, redirect to login page
        toast.info('Account created successfully! Please log in.');
        this.$router.push('/');
      }
    },
    redirectLogin() {

      this.$router.push('/');
    },


  },
};
</script>


<style scoped>
.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  position: relative;
  background-image: url("@/assets/LoginPage.png");
  background-position: center;
  padding: 0 16px;
}

/* Success Animation Styles */
.success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(7, 94, 84, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.5s ease-in-out;
}

.success-animation {
  text-align: center;
  color: white;
  animation: slideUp 0.8s ease-out;
}

.success-icon {
  margin-bottom: 30px;
}

.checkmark {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: block;
  stroke-width: 2;
  stroke: #fff;
  stroke-miterlimit: 10;
  margin: 0 auto;
  box-shadow: inset 0px 0px 0px #fff;
  animation: fill 0.4s ease-in-out 0.4s forwards, scale 0.3s ease-in-out 0.9s both;
}

.checkmark-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #fff;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

.success-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 15px;
  animation: fadeInUp 0.6s ease-out 0.3s both;
}

.success-message {
  font-size: 1.1rem;
  margin-bottom: 30px;
  opacity: 0.9;
  animation: fadeInUp 0.6s ease-out 0.5s both;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  animation: fadeInUp 0.6s ease-out 0.7s both;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  animation: bounce 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

/* Keyframe Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}

@keyframes fill {
  100% {
    box-shadow: inset 0px 0px 0px 30px #fff;
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Responsive padding for different screen sizes */
@media (min-width: 640px) {

  /* equivalent to sm:px-6 */
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {

  /* equivalent to lg:px-8 */
  .container {
    padding: 0 32px;
  }
}
</style>