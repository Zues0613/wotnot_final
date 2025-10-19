<template>
  <div class="flex flex-col m-8 overflow-y-auto h-[80vh] md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Profile Settings</h2>
        <p>Change your business profile details</p>
      </div>
    </div>

    <div class="w-full max-w-3xl space-y-6">
      <div class="flex">
        <div>
          <img
            :src="profile.profile_picture_url"
            alt="Description of image"
            style="
              width: 100px;
              height: 100px;
              object-fit: cover;
              object-position: start;
              display: block;
              border-radius: 4px;
            "
          />
          <img :scr="profile.profile_picture_url" />

          <h3 class="block mb-2 font-bold">Profile Picture</h3>
        </div>

        <div class="flex flex ml-4 items-center max-w-[50px]">
          <input type="file" @change="handleFileChange" class="mb-4" />

          <div>
            <button
              @click="uploadFile"
              :disabled="!selectedFile || isUploading"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-400"
            >
              {{ isUploading ? "Uploading..." : "Upload" }}
            </button>
          </div>

          <div
            v-if="uploadResponse"
            class="mt-4 p-2 bg-green-100 border border-green-300 rounded"
          >
            <p class="text-sm text-green-700">Upload Successful!</p>
          </div>

          <div
            v-if="uploadError"
            class="mt-4 p-2 bg-red-100 border border-red-300 rounded"
          >
            <p class="text-sm text-red-700">Error: {{ uploadError }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="about" class="block mb-2 font-bold">About</label>
          <input
            id="about"
            type="text"
            v-model="profile.about"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
        <div>
          <label for="businessAddress" class="block mb-2 font-bold"
            >Business Address</label
          >
          <input
            id="businessAddress"
            type="text"
            v-model="profile.address"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessDescription" class="block mb-2 font-bold"
            >Business Description</label
          >
          <textarea
            id="businessDescription"
            v-model="profile.description"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500 resize-none"
          ></textarea>
        </div>
        <div>
          <label for="businessEmail" class="block mb-2 font-bold"
            >Email for Business Contact</label
          >
          <input
            id="businessEmail"
            type="email"
            v-model="profile.email"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessIndustry" class="block mb-2 font-bold"
            >Business Industry</label
          >
          <select
            id="businessIndustry"
            v-model="profile.vertical"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          >
            <option value="TECH">Tech</option>
            <option value="BEAUTY">Beauty</option>
            <option value="HEALTH">Health</option>
            <option value="EDU">Education</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <div>
          <label for="websites" class="block mb-2 font-bold"
            >Websites (comma-separated)</label
          >
          <input
            id="websites"
            type="text"
            v-model="profile.websites"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="flex justify-end space-x-4">
        <button
          type="button"
          @click="resetProfile"
          class="bg-gray-300 text-white rounded px-6 py-2 hover:bg-gray-400 transition"
        >
          Reset
        </button>
        <button
          type="button"
          @click="updateProfile"
          class="bg-green-500 text-white rounded px-6 py-2 hover:bg-green-600 transition"
        >
          Save
        </button>
      </div>
    </div>
    <div>
      <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
        <div>
          <h2 class="text-xl md:text-2xl font-bold">Signup for API</h2>
          <p>Signup with facebook to get Whatsapp API</p>
        </div>
      </div>

      <!-- fb-signup -->
      <div>
        <div id="fb-root"></div>
        <button
          @click="launchWhatsAppSignup"
          style="
            background-color: #1877f2;
            border: 0;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
            font-family: Helvetica, Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            height: 40px;
            padding: 0 24px;
          "
        >
          Login with Facebook
        </button>
        <!-- <p>Session info response:</p>
                <pre>{{ sessionInfoResponse }}</pre>
                <br />
                <p>SDK response:</p>
                <pre>{{ sdkResponse }}</pre> -->
      </div>
    </div>
  </div>
</template>

<script>
/* global FB */
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,

      selectedFile: null,
      isUploading: false,
      uploadResponse: null,
      uploadError: null,
      uploadHandleID: null,

      profile: {
        about: "",
        address: "",
        email: "",
        description: "",
        websites: "",
        vertical: "OTHER",
        messaging_product: "whatsapp",
        profile_picture_url: "", // Default value
      },
      originalProfile: {}, // For reset functionality
      loading: true,

      // fb-signup
      sessionInfoResponse: "",
      sdkResponse: "",
    };
  },
  async mounted() {
    await this.fetchProfile();
    document.addEventListener("click", this.handleOutsideClick);
    
    // Check if we're returning from Facebook OAuth
    this.handleFacebookCallback();

    const checkAndSend = () => {
      if (this.sessionInfoResponse && this.sdkResponse) {
        // Send data to the backend
        fetch(`${this.apiUrl}/subscribe_customer`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
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

    // Watch for changes in both variables
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

    // Initialize the Facebook SDK
    window.fbAsyncInit = () => {
      try {
        FB.init({
          appId: process.env.VUE_APP_FACEBOOK_APP_ID || "2621821927998797",
          autoLogAppEvents: false, // Disable auto logging to prevent network errors
          xfbml: false, // Disable xfbml to prevent additional network calls
          version: "v21.0",
          cookie: true,
          status: false, // Disable status checking
        });
        console.log('Facebook SDK initialized successfully');
      } catch (error) {
        console.error('Error initializing Facebook SDK:', error);
      }
    };

    // Dynamically load the Facebook SDK
    const script = document.createElement("script");
    script.src = "https://connect.facebook.net/en_US/sdk.js";
    script.async = true;
    script.defer = true;
    script.crossOrigin = "anonymous";
    
    // Add error handling for script loading
    script.onerror = () => {
      console.error('Failed to load Facebook SDK');
      alert('Failed to load Facebook SDK. Please check your internet connection and try again.');
    };
    
    script.onload = () => {
      console.log('Facebook SDK script loaded successfully');
    };
    
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

  methods: {
    fbLoginCallback(response) {
      console.log("Facebook login response:", response);
      
      if (response.authResponse) {
        const code = response.authResponse.code;
        console.log("Auth Response Code:", code);
        
        // Send the code to backend for processing
        this.sendCodeToBackend(code);
      } else if (response.error) {
        console.error("Facebook login error:", response.error);
        alert(`Facebook login failed: ${response.error.message}`);
      }
      
      this.sdkResponse = JSON.stringify(response, null, 2);
    },

    async sendCodeToBackend(code) {
      try {
        console.log("Sending code to backend:", code);
        console.log("Session info response:", this.sessionInfoResponse);
        console.log("SDK response:", this.sdkResponse);
        
        const token = localStorage.getItem("token");
        const response = await fetch(`${this.apiUrl}/subscribe_customer`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sessionInfoResponse: this.sessionInfoResponse,
            sdkResponse: this.sdkResponse,
          }),
        });

        console.log("Backend response status:", response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log("Backend response:", data);
          alert("WhatsApp Business Account connected successfully!");
          // Refresh the page to show updated status
          window.location.reload();
        } else {
          const errorData = await response.json();
          console.error("Backend error:", errorData);
          alert(`Failed to connect WhatsApp: ${errorData.detail || 'Unknown error'}`);
        }
      } catch (error) {
        console.error("Error sending code to backend:", error);
        alert("Failed to connect to backend server");
      }
    },

    launchWhatsAppSignup() {
      // Facebook SDK requires HTTPS, so we'll use the alternative method directly
      console.log('Using alternative Facebook OAuth method (HTTPS required)');
      this.launchWhatsAppSignupAlternative();
    },

    launchWhatsAppSignupAlternative() {
      // Alternative method using direct URL redirect
      const appId = process.env.VUE_APP_FACEBOOK_APP_ID || "2621821927998797";
      const configId = process.env.VUE_APP_FACEBOOK_CONFIG_ID || "951833230236631";
      const redirectUri = encodeURIComponent(window.location.origin + '/settings');
      
      // Use the WhatsApp Business API OAuth endpoint
      const facebookUrl = `https://www.facebook.com/v21.0/dialog/oauth?` +
        `client_id=${appId}&` +
        `redirect_uri=${redirectUri}&` +
        `response_type=code&` +
        `scope=whatsapp_business_management,whatsapp_business_messaging&` +
        `config_id=${configId}&` +
        `setup[whatsapp_business_management][business_verification][mode]=DEVELOPMENT`;
      
      console.log('Redirecting to Facebook WhatsApp Business API:', facebookUrl);
      window.location.href = facebookUrl;
    },

    handleFacebookCallback() {
      // Check if we have a code in the URL (returning from Facebook)
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const error = urlParams.get('error');
      
      if (error) {
        console.error('Facebook OAuth error:', error);
        alert(`Facebook login failed: ${error}`);
        return;
      }
      
      if (code) {
        console.log('Received authorization code from Facebook:', code);
        // Create a mock response object similar to what FB.login would return
        const mockResponse = {
          authResponse: {
            code: code
          }
        };
        this.fbLoginCallback(mockResponse);
        
        // Clean up the URL
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    },

    loadFacebookSDK() {
      if (!document.getElementById("facebook-jssdk")) {
        const script = document.createElement("script");
        script.id = "facebook-jssdk";
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
          appId: process.env.VUE_APP_FACEBOOK_APP_ID || "2621821927998797", // From environment variable
          cookie: true,
          xfbml: true,
          version: "v20.0",
        });
        this.renderFacebookButton();
      };
    },
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `${this.apiUrl}/get-business-profile/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (
          response.status >= 200 &&
          response.status < 300 &&
          response.data.data.length
        ) {
          const data = response.data.data[0]; // Access the first object in the "data" array
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
          this.originalProfile = { ...this.profile }; // Save original profile for reset
        }
      } catch (error) {
        console.error(
          "Error fetching profile:",
          error.response?.data?.detail || error.message
        );
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      const toast = useToast();
      try {
        const token = localStorage.getItem("token");
        const payload = {
          about: this.profile.about,
          address: this.profile.address,
          email: this.profile.email,
          description: this.profile.description,
          websites: this.profile.websites
            ? this.profile.websites.split(",").map((site) => site.trim()) // Convert websites to an array
            : [], // Default to an empty array if no websites are provided
          vertical: this.profile.vertical || "OTHER", // Ensure a default value
          messaging_product: this.profile.messaging_product || "whatsapp", // Default to "whatsapp"
          profile_picture_handle: this.uploadHandleID || "", // Ensure handle ID is assigned
        };

        const response = await axios.post(
          `${this.apiUrl}/update-profile/`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status >= 200 && response.status < 300) {
          toast.success("Profile updated successfully!");
          await this.fetchProfile(); // Update originalProfile after successful save
        }
      } catch (error) {
        toast.error("Failed to update profile!");
        console.error(
          "Error updating profile:",
          error.response?.data?.detail || error.message
        );
      }
    },
    resetProfile() {
      this.profile = { ...this.originalProfile }; // Reset to original data
    },

    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file first.");
        return;
      }

      this.isUploading = true;
      this.uploadResponse = null;
      this.uploadError = null;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const token = localStorage.getItem("token"); // Adjust based on your auth storage
        const response = await axios.post(
          `${this.apiUrl}/resumable-upload/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.uploadResponse = response.data;
        this.uploadHandleID = response.data.upload_response?.h || "N/A";
        console.log(this.uploadHandleID);
      } catch (error) {
        this.uploadError = error.response
          ? error.response.data.detail
          : "Upload failed";
      } finally {
        this.isUploading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
