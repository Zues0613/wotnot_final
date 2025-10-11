<template>
  <div class="p-4 sm:p-6">
    <MessageGenerator class="mb-8" @message-generated="handleGeneratedMessage" />
    <div class="flex flex-col items-start justify-between gap-4 pb-5 mb-4 border-b md:flex-row md:items-center">
      <div>
        <h2 class="text-xl font-bold md:text-2xl">Manage Templates</h2>
        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>
      <div>
        <button
          class="flex items-center justify-center px-6 py-3 font-medium text-white transition-all duration-300 bg-green-700 rounded-lg shadow-lg hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478]"
          @click="showPopup = true">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
          </svg>
          New Template
        </button>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="flex items-center gap-2 mb-6">
      <button 
        @click="activeTab = 'templates'"
        :class="activeTab === 'templates' 
          ? 'bg-green-700 text-white shadow-md' 
          : 'bg-white text-gray-700 border border-gray-300 hover:border-green-500 hover:bg-green-50'"
        class="px-6 py-2.5 rounded-lg transition-all duration-200 font-medium">
        <span class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Templates
          <span v-if="cursor" class="inline-block w-4 h-4 border-2 border-white rounded-full border-t-transparent animate-spin"></span>
        </span>
      </button>
      
      <button 
        @click="activeTab = 'recycle'; fetchDeletedTemplates()"
        :class="activeTab === 'recycle' 
          ? 'bg-orange-600 text-white shadow-md' 
          : 'bg-white text-gray-700 border border-gray-300 hover:border-orange-500 hover:bg-orange-50'"
        class="px-6 py-2.5 rounded-lg transition-all duration-200 font-medium relative">
        <span class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          Recycle Bin
          <span v-if="deletedTemplates.length > 0" class="ml-1 px-2 py-0.5 text-xs font-bold text-orange-600 bg-orange-100 rounded-full border border-orange-300">{{ deletedTemplates.length }}</span>
        </span>
      </button>
    </div>

    <!-- Templates Tab Content -->
    <div v-show="activeTab === 'templates'">
      <h3 class="mb-4 text-xl text-gray-600 md:text-2xs"><b>Template List</b></h3>

    <!-- Show empty state when no templates -->
    <div v-if="!cursor && templates.length === 0" class="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <svg class="w-20 h-20 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No Templates Yet</h3>
      <p class="text-gray-500 mb-4 text-center">Get started by creating your first message template</p>
      <button
        class="flex items-center justify-center px-6 py-3 font-medium text-white bg-green-700 rounded-lg shadow-lg hover:bg-green-600"
        @click="showPopup = true">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
        </svg>
        Create First Template
      </button>
    </div>

    <!-- Show table when templates exist -->
    <div v-if="templates.length > 0" class="mb-2 overflow-x-auto custom-scrollbar max-h-[55vh]">
      <table class="w-full text-sm bg-white border border-gray-300 rounded-lg md:text-base"
        :class="{ 'opacity-50 pointer-events-none': tableLoading }">
        <thead>
          <tr class="font-semibold text-center text-gray-700 bg-gray-100">
            <th class="sticky top-0 z-10 p-3 text-left bg-gray-100 border border-gray-300 md:p-4">Name</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Language</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Status</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Category</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Sub Category</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">ID</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Preview</th>
            <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Actions</th>
          </tr>
        </thead>
        <tbody class="">
          <tr v-for="template in templates" :key="template.id" class="hover:bg-gray-50">
            <td class="p-3 text-left border border-gray-200 md:p-4">{{ template.name }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ template.language }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <div :class="{
                ' text-green-600 font-semibold px-2 py-1 rounded': template.status === 'APPROVED',
                ' text-blue-600 font-semibold px-2 py-1 rounded': template.status === 'PENDING',
                ' text-red-500 font-semibold px-2 py-1 rounded': template.status === 'REJECTED'
              }">
                {{ template.status }}
              </div>
            </td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ template.category }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ template.sub_category }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ template.id }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <button class="font-medium text-gray-600 underline hover:bg-inherit hover:text-gray-800"
                @click="showpreview(template.preview)">
                Preview
              </button>
            </td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <button @click="showConfirmationPopup(template.name)" class="p-2 transition rounded-full hover:bg-white">
                <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                  colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                </lord-icon>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    </div>

    <!-- Recycle Bin Tab Content -->
    <div v-show="activeTab === 'recycle'">
      <h3 class="mb-4 text-xl text-orange-600 md:text-2xs">
        <b>Recycle Bin</b>
        <span v-if="recycleBinLoading" class="inline-block w-5 h-5 ml-5 border-2 border-orange-500 rounded-full border-t-transparent animate-spin"></span>
      </h3>

      <!-- Empty Recycle Bin State -->
      <div v-if="!recycleBinLoading && deletedTemplates.length === 0" class="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <svg class="w-20 h-20 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
        </svg>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">Recycle Bin is Empty</h3>
        <p class="text-gray-500 text-center">Deleted templates will appear here and can be restored</p>
      </div>

      <!-- Deleted Templates Table -->
      <div v-if="deletedTemplates.length > 0" class="overflow-x-auto custom-scrollbar max-h-[55vh]">
        <table class="w-full text-sm bg-white border border-gray-300 rounded-lg md:text-base">
          <thead>
            <tr class="font-semibold text-center text-gray-700 bg-gray-100">
              <th class="sticky top-0 z-10 p-3 text-left bg-gray-100 border border-gray-300 md:p-4">Name</th>
              <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Category</th>
              <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Deleted At</th>
              <th class="sticky top-0 z-10 p-3 border border-gray-300 bg-gray-100 md:p-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="template in deletedTemplates" :key="template.id" class="hover:bg-gray-50">
              <td class="p-3 text-left border border-gray-200 md:p-4">{{ template.name }}</td>
              <td class="p-3 text-center border border-gray-200 md:p-4">{{ template.category }}</td>
              <td class="p-3 text-center border border-gray-200 md:p-4">{{ formatDate(template.deleted_at) }}</td>
              <td class="p-3 text-center border border-gray-200 md:p-4">
                <div class="flex justify-center gap-2">
                  <!-- Restore Button -->
                  <button 
                    @click="restoreTemplate(template.name)"
                    class="px-3 py-1 text-sm font-medium text-white bg-green-600 rounded hover:bg-green-700 transition-colors"
                    title="Restore template">
                    <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    Restore
                  </button>
                  
                  <!-- Permanent Delete Button -->
                  <button 
                    @click="showPermanentDeleteConfirm(template.name)"
                    class="px-3 py-1 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700 transition-colors"
                    title="Permanently delete">
                    <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                    Delete Forever
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <confirmationPopup v-if="showConfirmPopup" @yes="deleteTemplate(deleteTemplateName)" @no="showConfirmPopup = false"
      @close="showConfirmPopup = false" />
    
    <confirmationPopup v-if="showPermanentDeletePopup" @yes="permanentDeleteTemplate(permanentDeleteName)" @no="showPermanentDeletePopup = false"
      @close="showPermanentDeletePopup = false" 
      message="⚠️ This will PERMANENTLY delete the template. This action cannot be undone. Are you sure?" />

    <PopUp_preview v-if="showPreview" @close="closePreview">
      <div
        class="flex flex-col aspect-[10/19] p-3 max-h-[670px] bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center custom-scrollbar">
        <div class="message">
          <span style="white-space: pre-line;" v-html="preview_data"></span>
        </div>
      </div>
    </PopUp_preview>

    <PopUp v-if="showPopup" @close="closePopup"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">
      <h2 class="text-xl font-semibold text-green-800 mb-4">Create Message Template</h2>
      <hr class="pb-4">
      <div>
        <div class="flex flex-col gap-4 lg:flex-row">
          <div class="w-full lg:flex-1 max-h-[70vh] overflow-y-auto custom-scrollbar">
            <form class="p-4" :class="{ 'opacity-50 pointer-events-none': isSubmitted }">
              <h4 class="text-green-800"><b>Template name and language</b></h4>
              <p class="mb-2 text-sm ">Categorize your template</p>
              <div class="grid grid-cols-1 gap-4 p-4 mb-2 bg-[#f5f6fa] sm:grid-cols-2 xl:grid-cols-3">
                <div>
                  <label class="block text-sm font-medium below-402:text-custom-small">Template Name
                    <span class="text-red-800">*</span>
                  </label>
                  <div class="relative mb-2">
                    <input v-model="template.name" :placeholder="'Template Name'" @blur="validateTemplateName"
                      class="w-full h-10 p-2 mt-1 border border-gray-300 rounded-md" required />
                    <span v-if="nameError" class="absolute top-full left-0 mt-1 text-xs text-red-500">
                      {{ nameError }}</span>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium">Category<span class="text-red-800">*</span></label>
                  <select v-model="selectedCategory"
                    class="w-full h-10 p-2 mt-1 border border-gray-300 rounded-md" required>
                    <option value="Marketing">Marketing</option>
                    <option value="Utility">Utility</option>
                  </select>
                </div>
                <div class="mb-4">
                  <label class="block text-sm font-medium">Language<span class="text-red-800">*</span></label>
                  <select v-model="selectedLanguage"
                    class="w-full h-10 p-2 mt-1 border border-gray-300 rounded-md" required>
                    <option value="af">Afrikaans</option>
                    <option value="sq">Albanian</option>
                    <option value="ar">Arabic</option>
                    <option value="az">Azerbaijani</option>
                    <option value="bn">Bengali</option>
                    <option value="bg">Bulgarian</option>
                    <option value="ca">Catalan</option>
                    <option value="zh_CN">Chinese (Simplified)</option>
                    <option value="zh_HK">Chinese (Hong Kong)</option>
                    <option value="zh_TW">Chinese (Taiwan)</option>
                    <option value="hr">Croatian</option>
                    <option value="cs">Czech</option>
                    <option value="da">Danish</option>
                    <option value="nl">Dutch</option>
                    <option value="en">English</option>
                    <option value="en_GB">English (UK)</option>
                    <option value="en_US" default>English (US)</option>
                    <option value="et">Estonian</option>
                    <option value="fil">Filipino</option>
                    <option value="fi">Finnish</option>
                    <option value="fr">French</option>
                    <option value="ka">Georgian</option>
                    <option value="de">German</option>
                    <option value="el">Greek</option>
                    <option value="gu">Gujarati</option>
                    <option value="ha">Hausa</option>
                    <option value="he">Hebrew</option>
                    <option value="hi">Hindi</option>
                    <option value="hu">Hungarian</option>
                    <option value="id">Indonesian</option>
                    <option value="ga">Irish</option>
                    <option value="it">Italian</option>
                    <option value="ja">Japanese</option>
                    <option value="kn">Kannada</option>
                    <option value="kk">Kazakh</option>
                    <option value="rw_RW">Kinyarwanda</option>
                    <option value="ko">Korean</option>
                    <option value="ky_KG">Kyrgyz (Kyrgyzstan)</option>
                    <option value="lo">Lao</option>
                    <option value="lv">Latvian</option>
                    <option value="lt">Lithuanian</option>
                    <option value="mk">Macedonian</option>
                    <option value="ms">Malay</option>
                    <option value="ml">Malayalam</option>
                    <option value="mr">Marathi</option>
                    <option value="nb">Norwegian</option>
                    <option value="fa">Persian</option>
                    <option value="pl">Polish</option>
                    <option value="pt_BR">Portuguese (Brazil)</option>
                    <option value="pt_PT">Portuguese (Portugal)</option>
                    <option value="pa">Punjabi</option>
                    <option value="ro">Romanian</option>
                    <option value="ru">Russian</option>
                    <option value="sr">Serbian</option>
                    <option value="sk">Slovak</option>
                    <option value="sl">Slovenian</option>
                    <option value="es">Spanish</option>
                    <option value="es_AR">Spanish (Argentina)</option>
                    <option value="es_ES">Spanish (Spain)</option>
                    <option value="es_MX">Spanish (Mexico)</option>
                    <option value="sw">Swahili</option>
                    <option value="sv">Swedish</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                    <option value="th">Thai</option>
                    <option value="tr">Turkish</option>
                    <option value="uk">Ukrainian</option>
                    <option value="ur">Urdu</option>
                    <option value="uz">Uzbek</option>
                    <option value="vi">Vietnamese</option>
                    <option value="zu">Zulu</option>
                  </select>
                </div>
              </div>

              <h4 class="text-green-800"><b>Content</b></h4>
              <p class="mb-2 text-sm ">Fill in the header, body and footer sections of your template.</p>
              <div class="bg-[#f5f6fa] p-4">
                <div>
                  <label class="block text-sm font-medium">Header</label>
                  <select v-model="headerMediaComponent.format" class="w-full p-2 mb-2 border border-[#ddd] rounded-md">
                    <option value="TEXT">Text</option>
                    <option value="IMAGE">Image</option>
                    <option value="VIDEO">Video</option>
                  </select>
                  <div v-if="headerMediaComponent.format === 'TEXT'">
                    <input v-model="headerComponent.text" class="w-full p-2 mb-2 border border-[#ddd] rounded-md" />
                  </div>
                  <div v-if="headerMediaComponent.format === 'IMAGE' || headerMediaComponent.format === 'VIDEO'">
                    <div class="flex flex-col justify-between w-full sm:flex-row place-items-stretch">
                      <input type="file" @change="handleFileChange" class="mb-4">
                      <div>
                        <button @click="uploadFile" :disabled="!selectedFile || isUploading"
                          class="px-4 py-2 mr-5 text-white bg-green-700 rounded-lg hover:bg-green-800 disabled:cursor-not-allowed">
                          {{ isUploading ? 'Uploading...' : 'Upload' }}{{ uploadResponse ? 'ed' : '' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium">Body<span class="text-red-800">*</span></label>
                  <textarea v-model="bodyComponent.text"
                    class="w-full h-30 p-2 mt-1 border border-gray-300 rounded-md" placeholder="Enter text" rows="4"
                    required></textarea>
                  <div v-if="warningData"
                    class="p-3 mt-2 text-sm text-yellow-800 bg-yellow-100 border border-yellow-300 rounded-md">
                    <p class="font-semibold">Warning:{{ warningData }}</p>
                  </div>
                </div>
                <div class="flex items=flex-end justify-end">
                  <button type="button" @click="addVariable" class="p-2 font-bold text-black text-xs hover:bg-gray-200">
                    + Add variable
                  </button>
                </div>
                <div v-if="variables.length">
                  <h4></h4>
                  <label class="block text-sm font-medium">Samples for body content<span
                      class="text-red-800">*</span></label>
                  <span class="text-sm text-gray-500">To help us review your message template, please add an example for
                    each variable in your body text. Do not use real customer information. Cloud API hosted by Meta
                    reviews templates and variable parameters to protect the security and integrity of our
                    services.</span>
                  <div v-for="(variable, index) in variables" :key="index">
                    <input type="text" :placeholder="'Variable ' + (index + 1)" v-model="variables[index]"
                      class="w-50px p-2 mb-2 border border-[#ddd] rounded-md" required />
                  </div>
                </div>
                <label class="block text-sm font-medium">Footer</label>
                <input v-model="footerComponent.text" placeholder="Enter text"
                  class="w-full p-2 mb-2 border border-[#ddd] rounded-md" />
              </div>
              <h4 class="mt-2 text-green-800"><b>Buttons</b></h4>
              <p class="mb-2 text-sm ">Create buttons that let customers respond to your message or take action.</p>
              <div class="bg-[#f5f6fa] p-4 ">
                <span>
                  <button class="p-2 text-black border border-black text-small hover:bg-gray-200"
                    @click.prevent="addbutton">
                    + Add Button
                  </button>
                </span>
                <div class="mt-2">
                  <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text"
                    placeholder="Text" class="w-full p-2 mb-2 border border-[#ddd] rounded-md" />
                  <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url"
                    placeholder="URL" class="w-full p-2 mb-2 border border-[#ddd] rounded-md" />
                </div>
              </div>
              <button @click.prevent="submitTemplate"
                class="flex items-center justify-center px-6 py-3 mt-4 font-medium text-white bg-green-700 rounded-lg shadow-lg "
                :disabled="loading || isSubmitted">
                <span v-if="loading"
                  class="w-4 h-4 mr-2 border-2 border-white rounded-full border-t-transparent animate-spin"></span>
                {{ isSubmitted ? "Submitted" : loading ? "Submitting..." : "Submit" }}
              </button>
            </form>
          </div>
          <div
            class="w-full lg:w-1/3 aspect-[10/19] p-3 bg-[url('@/assets/chat-bg.jpg')] bg-cover bg-center rounded-lg shadow-inner">
            <div class="message">
              <span style="white-space: pre-line;" v-html="preview_data"></span>
            </div>
          </div>
        </div>
      </div>
    </PopUp>
  </div>
</template>

<script>

// import { QuillEditor } from '@vueup/vue-quill';
// import '@vueup/vue-quill/dist/vue-quill.snow.css';
import axios from 'axios';
import PopUp from "../popups/popup";
import { useToast } from 'vue-toastification';
import PopUp_preview from "../popups/template_preview";
import confirmationPopup from '../popups/confirmation';
import MessageGenerator from './MessageGenerator.vue';

export default {
  components: {
    // QuillEditor,
    PopUp_preview,
    confirmationPopup,
    PopUp,
    MessageGenerator
  },
  name: 'BroadCast1',
  props: {
    contactReport: {
      type: Object,
      required: false,
      default: () => ({})
    },
  },
  data() {
    return {

      cursor: false,
      apiUrl: process.env.VUE_APP_API_URL,
      selectedFile: null,
      isUploading: false,
      uploadResponse: null,
      uploadError: null,
      uploadHandleID: null,
      deleteTemplateName: '', // To store the name of the template to be deleted
      showConfirmPopup: false, // State to control the confirmation popup visibility
      
      // Recycle Bin
      activeTab: 'templates', // 'templates' or 'recycle'
      deletedTemplates: [],
      recycleBinLoading: false,
      showPermanentDeletePopup: false,
      permanentDeleteName: '',

      // loading
      loading: false, // Add loading state
      isSubmitted: false,
      tableLoading: false,

      showPreview: false,
      preview_data: '',
      tooltipVisible: false,
      tooltipStyles: {
        top: "0px",
        left: "0px",
        width: "170px", // Set square dimensions
        height: "100px",
      },
      templateName: '',
      isTemplateNameValid: true,
      templates: [],
      showPopup: false,
      addButton: false,
      showSelectionPopup: false,
      selectedCategory: 'Marketing',
      selectedSubCategory: '',
      selectedLanguage: 'en_US',
      selectedHeaderFormat: 'TEXT',
      template: {
        name: '',
        components: []
      },
      bodyComponent: {
        type: 'BODY',
        text: ''
      },
      headerComponent: {
        type: 'HEADER',
        format: 'TEXT',
        text: ''
      },
      headerMediaComponent: {
        type: 'HEADER',
        format: '',
        example: {
          header_handle: [
            ''
          ]
        }
      },
      footerComponent: {
        type: 'FOOTER',
        text: ''
      },
      button: {
        type: 'URL',
        text: '',
        url: ''
      },
      nameError: '',

      variableCounter: null,
      variables: [],
      warningData: null, // To store error data from the API
    };
  },
  async mounted() {
    await this.fetchtemplateList();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },

  methods: {

    handleGeneratedMessage(message) {
      this.bodyComponent.text = message;
      this.showPopup = true;
    },

    async showConfirmationPopup(templateName) {
      this.showConfirmPopup = true;
      this.deleteTemplateName = templateName;
    },

    addVariable() {
      const text = this.bodyComponent.text || '';
      const currentVariables = text.match(/{{\d+}}/g) || [];
      const nextVariableNumber = currentVariables.length + 1;
      this.bodyComponent.text += ` {{${nextVariableNumber}}}`;
      this.variableCounter = nextVariableNumber;
      while (this.variables.length < nextVariableNumber) {
        this.variables.push("");
      }
      console.log("Updated variable counter:", this.variableCounter);
      console.log("Updated variables:", this.variables);
    },

    showpreview(preview) {
      this.showPreview = true;
      this.preview_data = preview;
    },
    addbutton() {
      this.addButton = !this.addButton;
    },

    openPopup() {
      this.showPopup = true;
      this.selectedType = 'MARKETING';
    },


    async fetchtemplateList() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No token found, skipping template fetch');
        this.cursor = false;
        return;
      }

      this.cursor = true;
      try {
        const response = await fetch(`${this.apiUrl}/template`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          // Handle 401 gracefully - WhatsApp Business Account not configured
          if (response.status === 401) {
            console.warn('Unauthorized - WhatsApp Business Account not configured yet');
            this.templates = [];
            this.cursor = false;
            return;
          }
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data || [];
        this.cursor = false;

        this.templates = this.templates.map(template => {
          return {
            ...template,
            preview: this.generateTemplatePreview(template.components),
          };
        });
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
        this.templates = [];
        this.cursor = false;
      }
    },


    generateTemplatePreview(components) {

      if (!Array.isArray(components)) {
        console.warn("generateTemplatePreview: components is not an array", components);
        return '';
      }
      let previewMessage = '';

      components.sort((a, b) => {
        const order = { HEADER: 1, BODY: 2, FOOTER: 3, BUTTONS: 4 };
        return (order[a.type] || 5) - (order[b.type] || 5);
      });

      components.forEach(component => {
        switch (component.type) {
          case 'HEADER': {
            if (component.format === 'TEXT') {
              previewMessage += `<strong>${component.text}\n</strong> `;
            } else if (component.format === 'IMAGE' && component.example?.header_handle) {
              previewMessage += `<div style="width: auto; height: 200px; overflow: hidden; position: relative; border-radius: 5px">
  <img src="${component.example.header_handle[0]}" alt="Description of image" 
       style="width: 100%; height: 100%; object-fit: cover; object-position: start; display: block ; border-radius: 4px">
</div>`;

            }

            else if (component.format === 'VIDEO' && component.example?.header_handle) {
              previewMessage += `<div style="width: auto; height: 200px; overflow: hidden; position: relative; border-radius: 5px">
                <video controls 
                       src="${component.example.header_handle[0]}" 
                       style="width: 100%; height: 100%; object-fit: cover; object-position: start; display: block; border-radius: 4px">
                       Your browser does not support the video tag.
                </video>
            </div>`;
            }
            break;
          }
          case 'BODY': {
            let bodyText = component.text;
            bodyText = this.replacePlaceholders(bodyText, component.example?.body_text);
            previewMessage += bodyText;

            break;
          }
          case 'FOOTER': {
            previewMessage += `<span style="font-weight: lighter; color:gray;">\n${component.text}</span> `;
            break;
          }
          case 'BUTTONS': {
            if (component.buttons && Array.isArray(component.buttons)) {
              previewMessage += `<div style=" text-align: left;">`;
              component.buttons.forEach(button => {
                if (button.type === 'URL') {
                  previewMessage += `
        <a href="${button.url}" target="_blank" 
           style="display: inline-flex; align-items: center; 
                  text-decoration: none; font-weight: bold; color: #007bff; 
                   border-top: 1px solid #ddd;">
          <svg xmlns="http://www.w3.org/2000/svg" fill="#007bff" width="19" height="19" viewBox="0 0 24 24" style="margin-right: 5px;">
            <path d="M14 3v2h3.586l-8.293 8.293 1.414 1.414 8.293-8.293v3.586h2v-7h-7z"/>
            <path d="M5 5h6v-2h-6c-1.103 0-2 .897-2 2v14c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-6h-2v6h-14v-14z"/>
          </svg>
          <span style="padding:5px">${button.text}</span>
          
        </a>`;
                } else if (button.type === 'REPLY') {
                  previewMessage += `
        <button style="display: inline-block; margin: 5px 0; padding: 10px 15px; 
                       background-color: #007bff; color: white; border: none; 
                       border-radius: 20px; cursor: pointer; font-weight: bold;">
          ${button.text}
        </button>`;
                }
              });
              previewMessage += `</div>`;
            }
            break;
          }

          default: {
            previewMessage += `[Unknown Component Type] `;
            break;
          }
        }
      });

      return previewMessage;
    },

    replacePlaceholders(bodyText, example) {
      if (!bodyText || !Array.isArray(example) || example.length === 0) return bodyText;

      example.forEach((param, index) => {
        if (param && param.toString().trim() !== '') {
          const placeholder = `${index + 1}`;
          const regex = new RegExp(placeholder, 'g');
          bodyText = bodyText.replace(regex, param.toString().trim());
        }
      });

      return bodyText;
    },

    updateTemplateComponents() {
      const clonedBodyComponent = { ...this.bodyComponent };
      if (this.variables.length > 0) {
        clonedBodyComponent.example = { body_text: this.variables };
      }
      let components = [clonedBodyComponent];
      if (this.headerComponent.text) {
        components.push(this.headerComponent);
      }
      if (
        this.headerMediaComponent.example.header_handle &&
        this.headerMediaComponent.example.header_handle.length > 0 &&
        this.headerMediaComponent.example.header_handle[0] !== ''
      ) {
        components.push(this.headerMediaComponent);
      }
      if (this.footerComponent.text) {
        components.push(this.footerComponent);
      }
      if (this.button.text && this.button.url) {
        components.push({
          type: 'BUTTONS',
          buttons: [this.button]
        });
      }
      this.template.components = components;
      console.log(this.template);
    },

    async submitTemplate() {
      const toast = useToast();
      if (this.nameError) {
        return;
      }
      this.loading = true;
      const payload = {
        name: this.template.name,
        components: this.template.components,
        language: this.selectedLanguage,
        category: this.selectedCategory,
        sub_category: this.selectedSubCategory
      };
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No access token found in local storage');
        return;
      }
      try {
        const response = await axios.post(`${this.apiUrl}/create-template`, payload, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.status >= 200 && response.status < 300) {
          console.log('Template created successfully:', response.data);
          toast.success('Template created successfully');
          this.isSubmitted = true;
          await this.fetchtemplateList();

        } else {
          const errorMessage = response.data.detail || "Unknown error occurred";
          toast.error(`Error creating template: ${errorMessage}`);
          console.error('Error creating template:', response.data.detail);
        }
      } catch (error) {
        console.error('Full error object:', error);
        console.error('Error response:', error.response);
        
        let errorMessage = 'Unknown error occurred';
        
        if (error.response) {
          // Server responded with error status
          if (error.response.status === 401) {
            errorMessage = 'Session expired. Please login again.';
            // Optionally redirect to login
            setTimeout(() => {
              this.$router.push('/');
            }, 2000);
          } else if (error.response.data?.detail) {
            // Handle different detail formats
            if (typeof error.response.data.detail === 'string') {
              errorMessage = error.response.data.detail;
            } else if (error.response.data.detail?.error?.error_user_msg) {
              errorMessage = error.response.data.detail.error.error_user_msg;
            } else if (error.response.data.detail?.error?.message) {
              errorMessage = error.response.data.detail.error.message;
            } else {
              errorMessage = JSON.stringify(error.response.data.detail);
            }
          } else {
            errorMessage = `Error ${error.response.status}: ${error.response.statusText}`;
          }
        } else if (error.request) {
          // Request made but no response
          errorMessage = 'No response from server. Please check your connection.';
        } else {
          // Other errors
          errorMessage = error.message;
        }
        
        toast.error(`Request failed: ${errorMessage}`);
        console.error('Request failed:', error);
      }
      finally {
        this.loading = false;
      }
    },

    validateTemplateName() {
      this.template.name = this.template.name
        .toLowerCase()
        .replace(/\s+/g, '_')
        .trim();

      const regex = /^[a-z_0-9]+$/;

      if (this.template.name === '') {
        this.nameError = 'Template name is required';
      } else if (!regex.test(this.template.name)) {
        this.nameError = 'Template name must contain only lowercase letters, numbers, and underscores.';
      } else {
        this.nameError = '';
      }
    },

    async deleteTemplate(template_name) {
      this.showConfirmPopup = false;
      const toast = useToast();
      const token = localStorage.getItem('token');
      try {
        this.tableLoading = true;
        const response = await fetch(`${this.apiUrl}/delete-template/${template_name}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        const responseData = await response.json();

        if (response.ok && responseData.success) {
          toast.success('Template moved to recycle bin!');
          await this.fetchtemplateList(); // Refresh template list
          // Update recycle bin count if we're on that tab
          if (this.activeTab === 'recycle') {
            await this.fetchDeletedTemplates();
          }
        }
        else {
          const errorMessage = responseData.message || responseData.detail || "Failed to delete template";
          toast.error(`Error: ${errorMessage}`);
        }

      } catch (error) {
        console.error('Error deleting template:', error);
        toast.error('Failed to delete template. Please try again.');
      }
      finally {
        this.tableLoading = false;
        this.deleteTemplateName = '';
      }
    },

    async fetchDeletedTemplates() {
      const toast = useToast();
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No token found, skipping recycle bin fetch');
        return;
      }

      this.recycleBinLoading = true;
      try {
        const response = await fetch(`${this.apiUrl}/template/recycle-bin`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch recycle bin');
        }

        const data = await response.json();
        this.deletedTemplates = data.data || [];
        
      } catch (error) {
        console.error('Error fetching recycle bin:', error);
        toast.error('Failed to load recycle bin');
        this.deletedTemplates = [];
      } finally {
        this.recycleBinLoading = false;
      }
    },

    async restoreTemplate(template_name) {
      const toast = useToast();
      const token = localStorage.getItem('token');
      try {
        this.recycleBinLoading = true;
        const response = await fetch(`${this.apiUrl}/template/restore/${template_name}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        const responseData = await response.json();

        if (response.ok && responseData.success) {
          toast.success('Template restored successfully!');
          await this.fetchDeletedTemplates(); // Refresh recycle bin
          await this.fetchtemplateList(); // Refresh template list
        }
        else {
          const errorMessage = responseData.message || responseData.detail || "Failed to restore template";
          toast.error(`Error: ${errorMessage}`);
        }

      } catch (error) {
        console.error('Error restoring template:', error);
        toast.error('Failed to restore template. Please try again.');
      } finally {
        this.recycleBinLoading = false;
      }
    },

    showPermanentDeleteConfirm(template_name) {
      this.permanentDeleteName = template_name;
      this.showPermanentDeletePopup = true;
    },

    async permanentDeleteTemplate(template_name) {
      this.showPermanentDeletePopup = false;
      const toast = useToast();
      const token = localStorage.getItem('token');
      try {
        this.recycleBinLoading = true;
        const response = await fetch(`${this.apiUrl}/template/permanent-delete/${template_name}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        const responseData = await response.json();

        if (response.ok && responseData.success) {
          toast.success('Template permanently deleted!');
          await this.fetchDeletedTemplates(); // Refresh recycle bin
        }
        else {
          const errorMessage = responseData.message || responseData.detail || "Failed to delete template";
          toast.error(`Error: ${errorMessage}`);
        }

      } catch (error) {
        console.error('Error permanently deleting template:', error);
        toast.error('Failed to delete template. Please try again.');
      } finally {
        this.recycleBinLoading = false;
        this.permanentDeleteName = '';
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    closePopup() {
      this.showPopup = false;
      this.clearForm();
    },

    clearForm() {
      this.Loading = false;
      this.template.name = '';
      this.isSubmitted = false;
      this.variableCounter = null;
      this.template.components = [];
      this.bodyComponent.text = '';
      this.headerComponent.text = '';
      this.footerComponent.text = '';
      this.button.text = '';
      this.button.url = '';
      this.variables = [];
      this.addButton = false;
      this.selectedCategory = 'Marketing';
      this.selectedSubCategory = '';
      this.selectedLanguage = 'en_US';
      this.nameError = '';
      this.loading = false;
      this.preview_data = '';

    },

    closePreview() {
      this.showPreview = false;
      this.preview_data = '';
    },

    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.uploadError = "No file selected for upload.";
        return;
      }

      this.isUploading = true;
      this.uploadResponse = null;
      this.uploadError = null;

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(`${this.apiUrl}/resumable-upload/`, formData, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        });

        this.uploadResponse = response.data;
        this.headerMediaComponent.example.header_handle[0] = response.data.upload_response?.h || "N/A";
        console.log(this.uploadHandleID);
      } catch (error) {
        this.uploadError = error.response ? error.response.data.detail : "Upload failed";
      } finally {
        this.isUploading = false;
      }
    },

    updateVariablesFromText(newText) {
      const placeholders = newText.match(/{{\d+}}/g) || [];
      const uniquePlaceholders = [...new Set(placeholders.map(p => parseInt(p.match(/\d+/)[0])))];
      const requiredLength = uniquePlaceholders.length;

      if (this.variables.length < requiredLength) {
        while (this.variables.length < requiredLength) {
          this.variables.push('');
        }
      } else if (this.variables.length > requiredLength) {
        this.variables.splice(requiredLength);
      }
      console.log("Updated variables:", this.variables);
    },

    validateTemplateText(newText) {
      const countWords = (text) => {
        if (!text) return 0;
        return text.split(/\s+/).filter(word => word.trim().length > 0).length;
      };

      const text = newText || '';
      const wordCount = countWords(text);
      const currentVariables = text.match(/{{\d+}}/g) || [];
      const variableCount = currentVariables.length;

      if (variableCount > 0) {
        const ratio = (wordCount - 1) / variableCount;
        if (ratio < 3) {
          this.warningData = "This template contains too many variable parameters relative to the message length. You need to decrease the number of variable parameters or increase the message length.";
        } else {
          this.warningData = null;
        }
      } else {
        this.warningData = null;
      }
    }
  },

  watch: {
    templateName() {
      this.validateTemplateName();
    },

    'bodyComponent.text'(newText) {
      this.updateVariablesFromText(newText);
      this.validateTemplateText(newText);
    },

    selectType(type) {
      this.selectedType = type;
      this.showSelectionPopup = false;
      this.showPopup = true;
    },

    closeSelectionPopup() {
      this.showSelectionPopup = false;
    },

    'template.components': {
      deep: true,
      handler(newComponents) {
        console.log("Updated Components:", newComponents);
        this.preview_data = this.generateTemplatePreview(newComponents);
      }
    },
    variables: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    bodyComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    headerComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    headerMediaComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    footerComponent: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    },
    button: {
      deep: true,
      handler() {
        this.updateTemplateComponents();
      }
    }
  },

};
</script>

<style scoped>
.message {
  font-size: small;
  display: flex;
  justify-content: space-between;
  background-color: #ffffff;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  max-width: 90%;
  min-width: 80px;
  height: auto;
  max-height: 650px;
  word-wrap: break-word;
  word-break: break-word;
  width: fit-content;
  overflow: hidden;

}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.quill-editor-wrapper .ql-container {
  display: flex;
  flex-direction: column-reverse;
  min-height: 200px;
  border: 1px solid #ccc;
}

.quill-editor-wrapper .ql-toolbar {
  border-top: 1px solid #ccc;
  border-bottom: none;
}

.quill-editor-wrapper .ql-editor {
  flex-grow: 1;
}
</style>
