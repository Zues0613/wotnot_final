<template>
  <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Message Generator 💬</h2>
    <div class="space-y-4">
      
      <div>
        <label for="prompt" class="block text-sm font-medium text-gray-700">1. Enter your prompt</label>
        <textarea
          id="prompt"
          v-model="prompt"
          rows="3"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="e.g., I am trying to send a diwali wish to my customers, can you please build a message."
        ></textarea>
      </div>
      <div>
        <button
          @click="generateMessage"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-[#075e54] via-[#089678] to-[#075e54] text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478] transition-all duration-300 disabled:opacity-50"
        >
          <span v-if="!isLoading">Generate Message</span>
          <div v-else class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating...
          </div>
        </button>
      </div>
      
      <div v-if="generatedMessage" class="mt-4 space-y-4 border-t pt-4">
        <h3 class="text-lg font-semibold text-gray-700">2. Template Details & Actions</h3>
        
        <div>
          <label for="generated-message" class="block text-sm font-medium text-gray-700">Generated Message</label>
          <textarea
            id="generated-message"
            v-model="generatedMessage"
            rows="5"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          ></textarea>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label for="template-name" class="block text-sm font-medium text-gray-700">Template Name</label>
                <input type="text" v-model="templateName" id="template-name" placeholder="e.g., diwali_wishes_2025" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                <p class="text-xs text-gray-500 mt-1">Use lowercase letters, numbers, and underscores.</p>
            </div>
            <div>
                <label for="template-category" class="block text-sm font-medium text-gray-700">Category</label>
                <select v-model="templateCategory" id="template-category" class="mt-1 block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    <option>MARKETING</option>
                    <option>UTILITY</option>
                    <option>AUTHENTICATION</option>
                </select>
            </div>
        </div>

        <div>
            <label for="csv-upload" class="block text-sm font-medium text-gray-700">Upload Contacts (Optional)</label>
            <input type="file" @change="handleFileUpload" id="csv-upload" accept=".csv" class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
            <p class="text-xs text-gray-500 mt-1">CSV must contain 'phone' and 'name' columns.</p>
            <div v-if="phoneNumbers" class="mt-2 text-sm font-medium text-green-600">
                ✅ Successfully loaded {{ Object.keys(phoneNumbers).length }} contacts.
            </div>
        </div>

        <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
            <button
              @click="createTemplate"
              :disabled="!isTemplateReady || isActionLoading"
              class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-blue-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isActionLoading">Create Template</span>
              <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            </button>
            <button
              @click="createAndSend"
              :disabled="!isSendReady || isActionLoading"
              class="w-full bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-green-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isActionLoading">Create & Send</span>
              <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            </button>
        </div>

        <div v-if="actionStatus" :class="actionStatus.isError ? 'text-red-600' : 'text-green-600'" class="mt-2 text-sm font-medium p-3 rounded-md" :style="{ backgroundColor: actionStatus.isError ? '#fee2e2' : '#dcfce7' }">
            {{ actionStatus.message }}
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import Papa from 'papaparse';

export default {
  name: 'MessageGenerator',
  data() {
    return {
      // The base URL for your API. Using the environment variable is best practice.
      // Make sure VUE_APP_API_URL is set to 'https://api.wotnot.skylog.in' in your .env file
      apiUrl: process.env.VUE_APP_API_URL || 'https://api.wotnot.skylog.in',
      prompt: '',
      generatedMessage: '',
      isLoading: false,

      templateName: '',
      templateCategory: 'MARKETING',
      phoneNumbers: null,
      isActionLoading: false,
      actionStatus: null,
    };
  },
  computed: {
    isTemplateReady() {
      return this.generatedMessage && this.templateName.trim() !== '';
    },
    isSendReady() {
      return this.isTemplateReady && this.phoneNumbers && Object.keys(this.phoneNumbers).length > 0;
    }
  },
  methods: {
    /**
     * Retrieves the auth token and builds the authorization header.
     * Returns the config object or null if the token is not found.
     */
    getAuthConfig() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No access token found in local storage');
        this.actionStatus = { message: 'Authentication error: You are not logged in.', isError: true };
        return null;
      }
      return {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      };
    },

    async generateMessage() {
      if (!this.prompt) return;

      const config = this.getAuthConfig();
      if (!config) return;

      this.isLoading = true;
      this.generatedMessage = '';
      this.actionStatus = null;

      try {
        const response = await axios.post(`${this.apiUrl}/api/generate-message`, {
          prompt: this.prompt,
        }, config); // Added auth config
        this.generatedMessage = response.data.message;
        this.$emit('message-generated', this.generatedMessage);
      } catch (error) {
        console.error('Error generating message:', error);
        this.actionStatus = { message: 'Failed to generate message.', isError: true };
      } finally {
        this.isLoading = false;
      }
    },
    
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.actionStatus = null;
      this.phoneNumbers = null;

      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        transformHeader: header => header.trim(),
        complete: (results) => {
          if (results.errors.length) {
            console.error('CSV parsing errors:', results.errors);
            this.actionStatus = { message: 'Error parsing CSV. Please ensure it is a valid CSV file.', isError: true };
            return;
          }
          
          const requiredHeaders = ['phone', 'name'];
          const actualHeaders = results.meta.fields; 
          if (!requiredHeaders.every(header => actualHeaders.includes(header))) {
            this.actionStatus = { message: `CSV must include '${requiredHeaders.join("' and '")}' columns.`, isError: true };
            return;
          }

          const phoneDict = {};
          for (const row of results.data) {
            const phone = row.phone?.trim();
            const name = row.name?.trim();
            if (phone && name) {
              phoneDict[phone] = name;
            }
          }
          
          if (Object.keys(phoneDict).length === 0) {
              this.actionStatus = { message: 'CSV processed, but no valid contacts with both phone and name were found.', isError: true };
              return;
          }

          this.phoneNumbers = phoneDict;
        },
        error: (error) => {
          console.error('Error parsing CSV:', error);
          this.actionStatus = { message: 'Failed to read or parse the CSV file.', isError: true };
        }
      });
    },

    buildTemplatePayload() {
      return {
        name: this.templateName.toLowerCase().replace(/\s+/g, '_'),
        language: "en_US",
        category: this.templateCategory,
        components: [{
          type: "BODY",
          text: this.generatedMessage,
        }],
      };
    },

    async createTemplate() {
      if (!this.isTemplateReady) return;

      const config = this.getAuthConfig();
      if (!config) return;

      this.isActionLoading = true;
      this.actionStatus = null;

      try {
        const payload = this.buildTemplatePayload();
        const response = await axios.post(`${this.apiUrl}/create-template`, payload, config); // Added auth config
        this.actionStatus = { message: `Template '${response.data.name}' created successfully with ID: ${response.data.id}`, isError: false };
      } catch (error) {
        console.error('Error creating template:', error);
        const detail = error.response?.data?.detail || 'An unknown error occurred.';
        this.actionStatus = { message: `Failed to create template: ${JSON.stringify(detail)}`, isError: true };
      } finally {
        this.isActionLoading = false;
      }
    },

    async createAndSend() {
      if (!this.isSendReady) return;
      
      const config = this.getAuthConfig();
      if (!config) return;

      this.isActionLoading = true;
      this.actionStatus = null;

      try {
        const fullPayload = {
          request: this.buildTemplatePayload(),
          phone_number_dict: this.phoneNumbers,
        };
        
        const response = await axios.post(`${this.apiUrl}/create-template/send`, fullPayload, config); // Added auth config
        this.actionStatus = { message: `Template created. Messages queued to ${response.data.queued_to.length} numbers.`, isError: false };

      } catch (error) {
        console.error('Error creating template and sending:', error);
        const detail = error.response?.data?.detail || 'An unknown error occurred.';
        this.actionStatus = { message: `Operation failed: ${JSON.stringify(detail)}`, isError: true };
      } finally {
        this.isActionLoading = false;
      }
    }
  },
};
</script>

<style scoped>

</style>
