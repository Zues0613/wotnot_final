<template>
  <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Message Generator</h2>
    <div class="space-y-4">
      <div>
        <label for="prompt" class="block text-sm font-medium text-gray-700">Enter your prompt</label>
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
          class="w-full bg-gradient-to-r from-[#075e54] via-[#089678] to-[#075e54] text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478] transition-all duration-300"
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
      <div v-if="generatedMessage">
        <label for="generated-message" class="block text-sm font-medium text-gray-700">Generated Message</label>
        <textarea
          id="generated-message"
          v-model="generatedMessage"
          rows="5"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        ></textarea>
        <button
          @click="copyToClipboard"
          class="mt-2 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg shadow-sm hover:bg-gray-300 transition-all duration-300"
        >
          Copy to Clipboard
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MessageGenerator',
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      prompt: '',
      generatedMessage: '',
      isLoading: false,
    };
  },
  methods: {
    async generateMessage() {
      if (!this.prompt) {
        return;
      }

      this.isLoading = true;
      this.generatedMessage = '';

      try {
        const response = await axios.post(`${this.apiUrl}/api/generate-message`, {
          prompt: this.prompt,
        });
        this.generatedMessage = response.data.message;
        this.$emit('message-generated', this.generatedMessage);
      } catch (error) {
        console.error('Error generating message:', error);
      } finally {
        this.isLoading = false;
      }
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.generatedMessage);
    },
  },
};
</script>

<style scoped>
</style>
