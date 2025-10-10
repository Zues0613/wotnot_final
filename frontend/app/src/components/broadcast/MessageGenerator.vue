<template>
  <div class="p-6 bg-gradient-to-br from-green-50 to-white rounded-lg shadow-lg border-2 border-green-100">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-green-800">AI Message Generator ✨</h2>
        <span class="px-3 py-1 text-xs font-semibold text-green-700 bg-green-100 rounded-full">Powered by DeepSeek</span>
      </div>
      <p class="text-sm text-gray-600 mt-2">Generate professional WhatsApp broadcast messages using AI</p>
    </div>

    <!-- Generator Form -->
    <form @submit.prevent="generateMessage" class="space-y-6">
      <!-- Prompt Input -->
      <div class="bg-white p-4 rounded-lg border border-gray-200">
        <label for="prompt" class="block text-sm font-semibold text-gray-700 mb-2">
          📝 Message Description <span class="text-red-500">*</span>
        </label>
        <textarea
          id="prompt"
          v-model="formData.prompt"
          rows="3"
          required
          placeholder="e.g., Diwali greetings for customers with a 20% discount offer"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          :disabled="loading"
        ></textarea>
        <p class="text-xs text-gray-500 mt-2">Describe what you want to say in your broadcast message</p>
      </div>

      <!-- Options Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Tone -->
        <div class="bg-white p-4 rounded-lg border border-gray-200">
          <label for="tone" class="block text-sm font-semibold text-gray-700 mb-2">🎭 Tone</label>
          <select
            id="tone"
            v-model="formData.tone"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            :disabled="loading"
          >
            <option value="informal">Informal & Friendly</option>
            <option value="formal">Formal & Professional</option>
          </select>
        </div>

        <!-- Length -->
        <div class="bg-white p-4 rounded-lg border border-gray-200">
          <label for="length" class="block text-sm font-semibold text-gray-700 mb-2">📏 Length</label>
          <select
            id="length"
            v-model="formData.length"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            :disabled="loading"
          >
            <option value="short">Short (1-2 sentences)</option>
            <option value="medium">Medium (4-5 sentences)</option>
            <option value="long">Long (7-9 sentences)</option>
          </select>
        </div>

        <!-- Placeholders -->
        <div class="bg-white p-4 rounded-lg border border-gray-200">
          <label for="placeholders" class="block text-sm font-semibold text-gray-700 mb-2">🏷️ Placeholders</label>
          <input
            id="placeholders"
            v-model="formData.placeholders"
            type="text"
            placeholder="e.g., name, discount, code"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            :disabled="loading"
          />
          <p class="text-xs text-gray-500 mt-1">Comma-separated (default: name)</p>
        </div>

        <!-- Audience -->
        <div class="bg-white p-4 rounded-lg border border-gray-200">
          <label for="audience" class="block text-sm font-semibold text-gray-700 mb-2">👥 Target Audience</label>
          <input
            id="audience"
            v-model="formData.audience"
            type="text"
            placeholder="e.g., VIP customers, new subscribers"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            :disabled="loading"
          />
        </div>
      </div>

      <!-- Generate Button -->
      <button
        type="submit"
        class="w-full bg-gradient-to-r from-green-600 via-green-700 to-green-600 text-white px-8 py-4 rounded-lg font-semibold flex items-center justify-center hover:from-green-700 hover:via-green-800 hover:to-green-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        :disabled="loading || !formData.prompt"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin h-5 w-5 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Generating with AI...
        </span>
        <span v-else class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          Generate Message
        </span>
      </button>
    </form>

    <!-- Generated Result -->
    <div v-if="result" class="mt-8 space-y-4 border-t-2 border-green-200 pt-6 animate-fadeIn">
      <!-- Result Header -->
      <div class="flex items-center justify-between bg-green-50 p-4 rounded-lg">
        <h3 class="text-lg font-bold text-green-800">✨ Generated Message</h3>
        <div class="flex gap-2 text-xs text-gray-600">
          <span class="px-2 py-1 bg-white rounded">{{ result.length }}</span>
          <span class="px-2 py-1 bg-white rounded">{{ result.source }}</span>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="result.error" class="p-4 bg-red-50 border-l-4 border-red-500 rounded">
        <p class="text-sm text-red-700"><strong>Error:</strong> {{ result.error }}</p>
      </div>

      <!-- Generated Text -->
      <div class="bg-white p-4 rounded-lg border border-gray-200">
        <label for="generatedText" class="block text-sm font-semibold text-gray-700 mb-2">
          Generated Message (Editable)
        </label>
        <textarea
          id="generatedText"
          v-model="result.message"
          rows="6"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Your AI-generated message will appear here..."
        ></textarea>
        <p class="text-xs text-gray-500 mt-2">
          💡 Tip: You can edit the message before using it. Keep placeholders like {name}.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-3">
        <button
          @click="copyToClipboard"
          class="flex-1 min-w-[200px] bg-white text-gray-700 px-6 py-3 rounded-lg font-medium border-2 border-gray-300 hover:bg-gray-50 transition-all duration-300 flex items-center justify-center"
          :disabled="!result.message"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
          </svg>
          {{ copied ? '✓ Copied!' : 'Copy to Clipboard' }}
        </button>

        <button
          @click="useMessage"
          class="flex-1 min-w-[200px] bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-lg font-medium hover:from-green-700 hover:to-green-800 transition-all duration-300 flex items-center justify-center shadow-lg"
          :disabled="!result.message"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          Use This Message
        </button>

        <button
          @click="generateMessage"
          class="px-6 py-3 bg-yellow-50 text-yellow-700 border-2 border-yellow-300 rounded-lg font-medium hover:bg-yellow-100 transition-all duration-300 flex items-center justify-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Retry
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessageGenerator',
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      loading: false,
      copied: false,
      result: null,
      formData: {
        prompt: '',
        tone: 'informal',
        length: 'medium',
        placeholders: '',
        audience: ''
      }
    }
  },
  methods: {
    async generateMessage() {
      if (!this.formData.prompt.trim()) {
        return
      }

      this.loading = true
      this.result = null
      this.copied = false

      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${this.apiUrl}/api/templates/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.formData)
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        this.result = data

        // Emit the generated message
        this.$emit('message-generated', data.message)

        if (!data.success) {
          console.error('Generation error:', data.error)
        }
      } catch (error) {
        console.error('Error generating message:', error)
        this.result = {
          success: false,
          message: '',
          source: 'error',
          error: error.message || 'Failed to generate message. Please try again.',
          prompt: this.formData.prompt,
          length: this.formData.length,
          placeholders: this.formData.placeholders,
          audience: this.formData.audience,
          metadata: {}
        }
      } finally {
        this.loading = false
      }
    },

    async copyToClipboard() {
      if (!this.result?.message) return

      try {
        await navigator.clipboard.writeText(this.result.message)
        this.copied = true
        setTimeout(() => {
          this.copied = false
        }, 2000)
      } catch (error) {
        console.error('Failed to copy:', error)
        alert('Failed to copy to clipboard')
      }
    },

    useMessage() {
      if (!this.result?.message) return
      this.$emit('message-used', this.result.message)
    }
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}
</style>
