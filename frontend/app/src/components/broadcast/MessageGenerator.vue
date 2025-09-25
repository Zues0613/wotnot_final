<template>
  <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Message Generator 📧</h2>
    <div class="space-y-4">

      <div>
        <label for="prompt" class="block text-sm font-medium text-gray-700">1. Describe the email you want to send</label>
        <textarea
          id="prompt"
          v-model="prompt"
          rows="3"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="e.g., A Diwali wish for my customers, including a 10% discount code."
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
        <h3 class="text-lg font-semibold text-gray-700">2. Review and Send Email</h3>

        <div>
            <label for="email-subject" class="block text-sm font-medium text-gray-700">Email Subject</label>
            <input type="text" v-model="emailSubject" id="email-subject" placeholder="e.g., Happy Diwali from OurTeam!" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
        </div>

        <div>
          <label for="generated-message" class="block text-sm font-medium text-gray-700">Email Body</label>
          <textarea
            id="generated-message"
            v-model="generatedMessage"
            rows="5"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          ></textarea>
        </div>

        <div>
          <h3 class="text-lg font-semibold text-gray-700 mt-4 mb-2">3. Import Contacts</h3>
          <div class="flex border-b">
              <button @click="importMethod = 'csv'" :class="importMethod === 'csv' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'" class="whitespace-nowrap py-2 px-4 border-b-2 font-medium text-sm">
                  Upload CSV
              </button>
              <button @click="importMethod = 'gsheet'" :class="importMethod === 'gsheet' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'" class="whitespace-nowrap py-2 px-4 border-b-2 font-medium text-sm">
                  Import from Google Sheet
              </button>
          </div>

          <div v-if="importMethod === 'csv'" class="mt-4">
              <label for="csv-upload" class="block text-sm font-medium text-gray-700">Upload Contacts from CSV</label>
              <input type="file" @change="handleFileUpload" id="csv-upload" accept=".csv" class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
              <p class="text-xs text-gray-500 mt-1">CSV file must contain 'email' and 'name' columns.</p>
          </div>

          <div v-if="importMethod === 'gsheet'" class="mt-4">
               <label for="gsheet-url" class="block text-sm font-medium text-gray-700">Public Google Sheet URL</label>
               <div class="flex space-x-2 mt-1">
                   <input type="url" v-model="googleSheetUrl" id="gsheet-url" placeholder="Paste your public Google Sheet URL here" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                   <button @click="handleGoogleSheetImport" :disabled="isActionLoading" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50">Import</button>
               </div>
               <p class="text-xs text-gray-500 mt-1">Sheet must be public and contain 'email' and 'name' columns.</p>
          </div>
            <div v-if="contacts" class="mt-2 text-sm font-medium text-green-600">
               ✅ Successfully loaded {{ Object.keys(contacts).length }} contacts.
           </div>
        </div>

        <button
          @click="sendEmails"
          :disabled="!isSendReady || isActionLoading"
          class="w-full bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-green-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="!isActionLoading">Send Emails</span>
          <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        </button>

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
      apiUrl: process.env.VUE_APP_API_URL || 'https://api.wotnot.skylog.in',
      prompt: '',
      generatedMessage: '',
      isLoading: false,

      // CHANGED: Renamed templateName to emailSubject for clarity
      emailSubject: '',
      // CHANGED: Renamed phoneNumbers to contacts
      contacts: null,
      isActionLoading: false,
      actionStatus: null,

      importMethod: 'csv', // 'csv' or 'gsheet'
      googleSheetUrl: '',
    };
  },
  computed: {
    isSendReady() {
        // CHANGED: Logic updated to use new property names
        return this.generatedMessage && this.emailSubject.trim() !== '' && this.contacts && Object.keys(this.contacts).length > 0;
    }
  },
  methods: {
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
        }, config);
        this.generatedMessage = response.data.message;
        this.$emit('message-generated', this.generatedMessage);
      } catch (error) {
        console.error('Error generating message:', error);
        this.actionStatus = { message: 'Failed to generate message.', isError: true };
      } finally {
        this.isLoading = false;
      }
    },
    
    parseCsvData(csvString) {
        Papa.parse(csvString, {
            header: true,
            skipEmptyLines: true,
            transformHeader: header => header.trim().toLowerCase(), // Make headers case-insensitive
            complete: (results) => {
                if (results.errors.length) {
                    console.error('CSV parsing errors:', results.errors);
                    this.actionStatus = { message: 'Error parsing data. Please ensure it is a valid CSV format.', isError: true };
                    return;
                }
                
                // CHANGED: Required headers updated to 'email'
                const requiredHeaders = ['email', 'name'];
                const actualHeaders = results.meta.fields;
                if (!requiredHeaders.every(header => actualHeaders.includes(header))) {
                    this.actionStatus = { message: `Data must include '${requiredHeaders.join("' and '")}' columns.`, isError: true };
                    return;
                }

                // CHANGED: Renamed to emailDict and logic updated to use 'email'
                const emailDict = {};
                for (const row of results.data) {
                    const email = row.email?.trim();
                    const name = row.name?.trim();
                    if (email && name) {
                        emailDict[email] = name;
                    }
                }

                if (Object.keys(emailDict).length === 0) {
                    this.actionStatus = { message: 'Data processed, but no valid contacts with both email and name were found.', isError: true };
                    return;
                }
                
                // CHANGED: Updated data property
                this.contacts = emailDict;
            },
            error: (error) => {
                console.error('Error parsing CSV string:', error);
                this.actionStatus = { message: 'Failed to read or parse the data.', isError: true };
            }
        });
    },

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.actionStatus = null;
        this.contacts = null;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.parseCsvData(e.target.result);
        };
        reader.onerror = () => {
             this.actionStatus = { message: 'Failed to read the file.', isError: true };
        };
        reader.readAsText(file);
    },
    
    async handleGoogleSheetImport() {
        if (!this.googleSheetUrl) {
            this.actionStatus = { message: 'Please enter a Google Sheet URL.', isError: true };
            return;
        }

        this.isActionLoading = true;
        this.actionStatus = null;
        this.contacts = null;

        try {
            const sheetIdMatch = this.googleSheetUrl.match(/spreadsheets\/d\/([a-zA-Z0-9-_]+)/);
            if (!sheetIdMatch || !sheetIdMatch[1]) {
                throw new Error("Invalid Google Sheet URL. Could not find Sheet ID.");
            }
            const sheetId = sheetIdMatch[1];
            const gidMatch = this.googleSheetUrl.match(/[#&]gid=([0-9]+)/);
            const gid = gidMatch ? gidMatch[1] : '0';
            const csvExportUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv&gid=${gid}`;
            
            this.actionStatus = { message: 'Fetching data from Google Sheet...', isError: false };

            const response = await axios.get(csvExportUrl);
            
            if (typeof response.data === 'string' && response.data.trim().startsWith('<!DOCTYPE html>')) {
                 throw new Error("Could not fetch data. Please ensure the Google Sheet is public ('Anyone with the link can view').");
            }
            
            this.parseCsvData(response.data);

        } catch (error) {
            console.error('Error importing from Google Sheet:', error);
            this.actionStatus = { message: error.message || 'Failed to import from Google Sheet.', isError: true };
        } finally {
            this.isActionLoading = false;
        }
    },

    buildEmailPayload() {
      // This helper builds the structure the new backend expects
      return {
        // The 'request' object contains the message details
        request: {
          name: this.emailSubject.toLowerCase().replace(/\s+/g, '_'),
          language: "en_US",
          category: "MARKETING", // Kept for schema consistency, but unused by SMTP backend
          components: [{
            type: "BODY",
            text: this.generatedMessage,
          }],
        },
        // CHANGED: The key is now 'email_dict'
        email_dict: this.contacts,
      };
    },

    async sendEmails() {
      if (!this.isSendReady) return;
      
      const config = this.getAuthConfig();
      if (!config) return;

      this.isActionLoading = true;
      this.actionStatus = null;

      try {
        const payload = this.buildEmailPayload();
        
        // CHANGED: Endpoint remains the same, but the payload is different
        const response = await axios.post(`${this.apiUrl}/create-template/send`, payload, config);
        
        // CHANGED: Success message updated for emails
        this.actionStatus = { message: `Emails have been successfully queued for ${response.data.queued_for.length} contacts.`, isError: false };

      } catch (error) {
        console.error('Error sending emails:', error);
        const detail = error.response?.data?.detail || 'An unknown error occurred.';
        this.actionStatus = { message: `Operation failed: ${JSON.stringify(detail)}`, isError: true };
      } finally {
        this.isActionLoading = false;
      }
    }
  },
};
</script>
