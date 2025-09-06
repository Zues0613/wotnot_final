<template>
  <div class="content-section flex flex-col h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white md:ml-64">
    <!-- Header -->
    <div class="fixed w-full flex items-center top-0 px-6 py-4 bg-white dark:bg-gray-800 border-b dark:border-gray-700 z-10">
      <div class="text-2xl font-bold">AI Assistant</div>
      <div class="ml-auto text-sm cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 px-3 py-2 rounded-md" @click="isConfigMode = !isConfigMode">
        Settings
      </div>
    </div>

    <!-- Chat Messages -->
    <div ref="chatList" class="flex-1 overflow-y-auto p-4 mt-16 mb-20 space-y-4">
      <div v-for="(msg, index) in messages" :key="index" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
        <div class="p-3 rounded-lg max-w-lg" :class="msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'">
          <p style="white-space: pre-wrap;">{{ msg.text }}</p>
        </div>
      </div>
    </div>

    <!-- Settings Mode -->
    <div v-if="isConfigMode" class="fixed bottom-0 w-full p-6 bg-white dark:bg-gray-800 border-t dark:border-gray-700">
      <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">Enter API Key:</div>
      <div class="flex">
        <input v-model="apiKey" class="flex-1 p-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg outline-none focus:ring-2 focus:ring-blue-500" type="password" placeholder="sk-xxxxxxxxxx"/>
        <button @click="saveApiKey" class="ml-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg">Save</button>
      </div>
    </div>

    <!-- Input Box -->
    <div v-else class="fixed bottom-0 w-full p-6 bg-white dark:bg-gray-800 border-t dark:border-gray-700 flex items-center md:pl-72 md:pr-10">
      <input v-model="inputMessage" @keydown.enter="sendMessage" class="flex-1 p-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg outline-none focus:ring-2 focus:ring-blue-500" placeholder="Type a message..."/>
      <button @click="sendMessage" class="ml-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg">Send</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  name: 'ManageTags',
  data() {
    return {
      messages: [
        { role: "assistant", text: "Hello! How can I assist you today?" }
      ],
      inputMessage: "",
      isConfigMode: false,
      apiKey: localStorage.getItem("apiKey") || "",
    };
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return;

      // Add user message
      this.messages.push({ role: "user", text: this.inputMessage });
      const userMessage = this.inputMessage;
      this.inputMessage = "";
      this.scrollToBottom();


      try {
        // Add a loading indicator for the assistant's response
        this.messages.push({ role: "assistant", text: "Thinking..." });
        this.scrollToBottom();

        const response = await axios.post("http://127.0.0.1:8000/chat", {
          message: userMessage,
        });

        // Replace "Thinking..." with the actual response
        this.messages.pop();
        this.messages.push({ role: "assistant", text: response.data.response });
      } catch (error) {
         this.messages.pop();
        this.messages.push({ role: "assistant", text: "Error connecting to the server. Please check if the local server is running." });
      }

      this.scrollToBottom();
    },
    saveApiKey() {
      localStorage.setItem("apiKey", this.apiKey);
      this.isConfigMode = false;
    },
    scrollToBottom() {
      nextTick(() => {
        const chatContainer = this.$refs.chatList;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    }
  },
  mounted() {
      this.scrollToBottom();
  }
};
</script>

<style scoped>
/* Scoped styles for the chat interface */
.content-section {
    transition: background-color 0.3s, color 0.3s;
}
</style>

