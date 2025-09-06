<template>
  <div class="p-4 sm:p-6">
    <div class="flex flex-col items-start justify-between gap-4 pb-5 mb-4 border-b md:flex-row md:items-center">
      <div>
        <h2 class="text-xl font-bold md:text-2xl ">Manage Contacts</h2>
        <p class="text-sm md:text-base">Contact list stores the list of numbers that you've interacted with.
          You can even manually export or import contacts.</p>
      </div>

      <div class="flex justify-between">
        <div>
          <button
            class="flex items-center justify-center px-6 py-3 font-medium text-white bg-green-700 rounded-lg shadow-lg hover:bg-green-600 "
            @click="showPopup = true">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
            </svg>
            New Contact
          </button>
        </div>
      </div>

      <confirmationPopup v-if="showConfirmPopup" @yes="deleteContact(this.selectedContact)"
        @no="showConfirmPopup = false" @close="showConfirmPopup = false" />
      <PopUp1 v-if="showPopupimport" @close="closePopupimport()">

        <h2 class="text-xl font-semibold mb-4">Bulk Import Contacts</h2>
        <hr class="mb-4 border-gray-300">

        <div class="overflow-y-auto max-h-[70vh] p-2 sm:p-6 custom-scrollbar space-y-6">
          <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <input type="file" @change="onFileChange" accept=".csv" class="w-full text-sm sm:w-auto" />
            <button :disabled="!file" @click="uploadFile"
              class="w-full h-10 px-4 text-green-500 transition duration-200 border-2 border-green-500 sm:w-24 hover:text-white hover:bg-green-500">
              Upload
            </button>
          </div>

          <div v-if="duplicates.length">
            <h4 class="mb-2 font-semibold text-green-700">Duplicate Contacts</h4>
            <div class="overflow-auto max-h-[30vh] custom-scrollbar">
              <table class="w-full text-sm bg-white border border-gray-300 rounded-lg table-fixed md:text-base">
                <thead>
                  <tr class="font-semibold text-center text-gray-700 bg-gray-100">
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/4">Name</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/3">Email</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/4">Phone</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/3">Tags</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(contact, index) in duplicates" :key="index">
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.name }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.email }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.phone }}</td>
                    <td class="p-2 text-left border border-gray-200">
                      <div class="truncate" v-for="(value, key) in contact.tags" :key="key">
                        {{ key }}: {{ value }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="importcontacts.length">
            <h4 class="mb-2 font-semibold text-green-700">New Contacts</h4>
            <div class="overflow-auto max-h-[30vh] custom-scrollbar">
              <table class="w-full text-sm bg-white border border-gray-300 rounded-lg table-fixed md:text-base">
                <thead>
                  <tr class="font-semibold text-center text-gray-700 bg-gray-100">
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/4">Name</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/3">Email</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/4">Phone</th>
                    <th class="sticky top-0 z-10 p-2 bg-gray-100 border border-gray-300 w-1/3">Tags</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(contact, index) in importcontacts" :key="index">
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.name }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.email }}</td>
                    <td class="p-2 text-left border border-gray-200 truncate">{{ contact.phone }}</td>
                    <td class="p-2 text-left border border-gray-200">
                      <div class="truncate" v-for="(value, key) in contact.tags" :key="key">
                        {{ key }}: {{ value }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="importcontacts.length" class="flex justify-end">
            <button :disabled="!file" @click="ImportCSV"
              class="h-10 px-4 text-green-500 transition duration-200 border-2 border-green-500 sm:w-24 hover:text-white hover:bg-green-500">
              Import
            </button>
          </div>
        </div>
      </PopUp1>
    </div>
    <PopUpSmall v-if="showPopup" @close="closePopup">
      <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Edit Contact' : 'Add Contact' }}</h2>
      <hr class="mb-4 border-gray-300">
      <form @submit.prevent="submitForm" id="contactForm" class="w-full max-w-md bg-white">
        <div class="p-4 bg-[#f5f6fa]">
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium">Name<span class="text-red-800">*</span></label>
            <input type="text" v-model="contact.name" id="name" placeholder="Name" required
              class="w-full px-3 py-2 border border-gray-300 rounded">
          </div>

          <div class="mb-4">
            <label for="phone" class="block text-sm font-medium">Phone Number<span class="text-red-800">*</span></label>
            <div class="flex">
              <select v-model="contact.countryCode" class="w-20 px-3 py-2 mr-2 border border-gray-300 rounded-l">
                <option value="1">+1</option>
                <option value="44">+44</option>
                <option value="91">+91</option>
              </select>
              <input type="text" v-model="contact.phone" id="phone" placeholder="Phone Number" required
                class="w-full px-3 py-2 border border-gray-300 rounded-r">
            </div>
          </div>
          <label for="email" class="block text-sm font-medium">Email</label>
          <input type="email" v-model="contact.email" id="email" placeholder="Email"
            class="w-full px-3 py-2 mb-2 border border-gray-300 rounded">

          <div class="mb-4">

            <div class="custom-scrollbar tags-container-container">
              <div class="tags-container">
                <div class="tag-input" v-for="(tag, index) in contact.tags" :key="index"
                  style="display: flex; align-items: center; gap: 10px;">
                  <input type="text" v-model="tag.key" placeholder="Key" required
                    class="w-full px-3 py-2 mb-2 border border-gray-300 rounded" style="flex: 1;">
                  <input type="text" v-model="tag.value" placeholder="Value" required
                    class="w-full px-3 py-2 mb-2 border border-gray-300 rounded" style="flex: 1;">
                  <button type="button" @click="removeTag(index)" class="p-2 transition rounded-full hover:bg-gray-100">
                    <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                      colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px"></lord-icon>
                  </button>
                  <span v-if="warningData" class="text-xs text-red-500">{{ warningData }}</span>
                </div>
              </div>
            </div>
            <button type="button" @click="addTag" class="p-2 text-black border border-black text-small hover:bg-gray-200">+
              Add
              Tag</button>

          </div>
        </div>


        <div class="flex justify-end pt-4 ">
          <button type="submit" class="px-4 py-2 text-white bg-green-700 rounded hover:bg-green-600">
            {{ isEditing ? 'Update Contact' : 'Add Contact' }}
          </button>
        </div>
      </form>
    </PopUpSmall>



    <div class="p-5 space-y-4 filter-container">

      <h3 class="mb-0 text-xl text-gray-600 md:text-2xs"><b>Contact List</b></h3>

      <div class="flex flex-col items-stretch justify-between gap-4 sm:flex-row sm:items-center">
        <div class="flex flex-col items-stretch gap-2 sm:flex-row sm:items-center">
          <h3 class="text-l"><b>Filter by tags:</b></h3>
          <input type="text" v-model="tag_key" placeholder="Key"
            class="w-full px-3 py-2 border border-gray-300 rounded sm:w-40">
          <input type="text" v-model="tag_value" placeholder="Value"
            class="w-full px-3 py-2 border border-gray-300 rounded sm:w-40">
          <button @click="fiterBytTags"
            class="relative w-full p-2 my-2 text-white bg-green-700 sm:w-auto hover:bg-green-600">Apply
            filter</button>
        </div>
        <div>
          <button @click="showPopupimport = true" class="w-full px-4 py-2 text-white bg-green-600 sm:w-auto hover:bg-green-700">
            <i class="bi bi-download"></i> Import CSV
          </button>
        </div>
      </div>
    </div>

    <div class="overflow-x-auto max-h-[51vh] custom-scrollbar">
      <table class="w-full text-sm bg-white border border-gray-300 rounded-lg md:text-base">
        <thead>
          <tr class="font-semibold text-center text-gray-700 bg-gray-100">
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">ID</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Name</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Phone Number</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Email</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Tags</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Created At</th>
            <th class="sticky top-0 z-10 p-3 bg-gray-100 border border-gray-300 md:p-4">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in contacts" :key="contact.id" class="hover:bg-gray-50">
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ contact.id }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ contact.name }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ contact.phone }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ contact.email }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <div v-for="(tag, index) in contact.tags" :key="index">
                <span class="font-semibold">{{ tag.key }}:</span> {{ tag.value }}
              </div>
            </td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ formatDate(contact.created_at) }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <div class="flex justify-center space-x-2">
                <button @click="modifyContact(contact)" class="p-2 transition rounded-full hover:bg-white">
                  <lord-icon src="https://cdn.lordicon.com/wuvorxbv.json" trigger="hover"
                    style="width:32px;height:32px">
                  </lord-icon>
                </button>
                <button @click="showConfirmationPopup(contact.phone)"
                  class="p-2 transition rounded-full hover:bg-white">
                  <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                    colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                  </lord-icon>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-center mt-4">
      <div class="flex items-center px-4 py-2 space-x-4 bg-white rounded-lg shadow-md">
        <button
          class="px-3 py-1 font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="loadPreviousPage" :disabled="currentPage === 1">
          Previous
        </button>
        <div class="px-4 py-1 font-semibold text-gray-700 border border-gray-300 rounded">
          {{ currentPage }}
        </div>
        <button class="px-3 py-1 font-medium text-white bg-green-600 rounded hover:bg-green-700" @click="loadNextPage">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp1 from "../popups/popup1";
import PopUpSmall from "../popups/popup_small";
import confirmationPopup from '../popups/confirmation';
import axios from "axios";

export default {
  components: {
    PopUp1,
    PopUpSmall,
    confirmationPopup
  },
  async mounted() {
    await this.fetchContactList();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  name: "ManageContacts",
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      currentPage: 1,
      showPopup: false,
      showPopupimport: false,
      showConfirmPopup: false,
      file: null,
      importcontacts: [],
      duplicates: [],
      contact: {
        id: "",
        name: "",
        email: "",
        phone: "",
        countryCode: "91",
        tags: [],
      },
      tag_key: '',
      tag_value: '',
      selectedContact: null,
      contacts: [],
      isEditing: false,
      warningData: '',
    };
  },
  methods: {
    showConfirmationPopup(phone) {
      this.selectedContact = phone;
      this.showConfirmPopup = true;
    },

    async loadNextPage() {
      const prev = this.contacts[0]?.id;
      await this.fetchContactList(this.currentPage + 1);
      const newFirst = this.contacts[0]?.id;
      if (prev !== newFirst && this.contacts.length > 0) {
        this.currentPage += 1;
      }
    },
    async loadPreviousPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        await this.fetchContactList(this.currentPage);
      }
    },

    async submitForm() {
      const toast = useToast();
      const { id, name, email, phone, countryCode, tags } = this.contact;

      let fullPhoneNumber = phone;
      if (countryCode && countryCode.trim() !== '') {
        fullPhoneNumber = `${countryCode}${phone}`;
      }

      if (tags.some(tag => tag.key === '' || tag.value === '')) {
        this.warningData = "Please enter key and value for all tags";
        return;
      }

      const tagArray = tags.map(tag => `${tag.key}:${tag.value}`);
      const url = id ? `${this.apiUrl}/contacts/${id}` : `${this.apiUrl}/contacts/`;
      const method = id ? "PUT" : "POST";
      const token = localStorage.getItem("token");

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name, email, phone: fullPhoneNumber, tags: tagArray }),
        });

        if (response.ok) {
          toast.success(id ? "Contact updated successfully" : "Contact created successfully");
          this.closePopup();
          await this.fetchContactList();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error saving contact:", error);
        toast.error("Error saving contact");
      }
    },
    clearForm() {
      this.contact = {
        id: "",
        name: "",
        email: "",
        phone: "",
        countryCode: "91",
        tags: [],
      };
      this.isEditing = false;
      this.warningData = '';
    },
    closePopup() {
      this.showPopup = false;
      this.clearForm();
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', options).replace(/,/g, '');
    },

    async fetchContactList(page = 1) {
      const token = localStorage.getItem("token");
      const itemsPerPage = 10;
      const url = `${this.apiUrl}/contacts/?sort_by=updated_at&order=desc&limit=${itemsPerPage}&offset=${(page - 1) * itemsPerPage}`;

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Network response was not ok");
        const contactsList = await response.json();
        if (contactsList.length === 0 && page > 1) {
          // You've reached the end
          this.currentPage = page - 1; // Revert page number
          return;
        }
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
          created_at: contact.created_at,
          updated_at: contact.updated_at
        }));
      } catch (error) {
        console.error("Error fetching contacts:", error);
      }
    },

    async fiterBytTags() {
      const token = localStorage.getItem("token");
      const tagValue = this.tag_value;
      const tagKey = this.tag_key;
      try {
        const response = await fetch(`${this.apiUrl}/contacts-filter/filter?tag_key=${tagKey}&tag_value=${tagValue}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        if (!response.ok) throw new Error("Network response not ok");
        const contactsList = await response.json();
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
          created_at: contact.created_at,
          updated_at: contact.updated_at
        }));
      } catch (error) {
        console.error("Error filtering contacts", error);
      }
    },
    modifyContact(contact) {
      this.isEditing = true;
      this.selectedContact = contact;
      this.contact = { ...contact, countryCode: '91' }; // Set default or extract from phone
      this.showPopup = true;
    },
    async deleteContact(phone) {
      const toast = useToast();
      this.showConfirmPopup = false;
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`${this.apiUrl}/contacts/${phone}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          toast.success("Contact deleted successfully");
          await this.fetchContactList(this.currentPage);
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error deleting contact:", error);
        toast.error("Error deleting contact");
      }
    },
    addTag() {
      this.warningData = "";
      const lastTag = this.contact.tags[this.contact.tags.length - 1];
      if (this.contact.tags.length === 0 || (lastTag && lastTag.key !== '' && lastTag.value !== '')) {
        this.contact.tags.push({ key: "", value: "" });
      } else {
        this.warningData = "Please fill out the previous tag first.";
      }
    },
    removeTag(index) {
      this.contact.tags.splice(index, 1);
    },
    onFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      if (!this.file) return;
      const formData = new FormData();
      const token = localStorage.getItem("token");
      formData.append("file", this.file);
      try {
        const response = await axios.post(`${this.apiUrl}/contacts/csv/`, formData, {
          headers: { "Content-Type": "multipart/form-data", Authorization: `Bearer ${token}` },
        });
        this.importcontacts = response.data.contacts || [];
        this.duplicates = response.data.duplicates || [];
      } catch (error) {
        console.error("Error uploading CSV:", error.response?.data?.detail || error.message);
      }
    },
    async ImportCSV() {
      const toast = useToast();
      if (!this.file) return;

      const formData = new FormData();
      const token = localStorage.getItem("token");
      formData.append("file", this.file);

      try {
        const response = await axios.post(`${this.apiUrl}/contacts/bulk_import/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.status >= 200 && response.status < 300) {
          toast.success("Contacts imported successfully");
          await this.fetchContactList();
          this.closePopupimport();
        } else {
          toast.error(`Error: ${response.data?.detail || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error importing contacts:", error.response?.data?.detail || error.message);
        toast.error(`Error: ${error.response?.data?.detail || "Something went wrong"}`);
      }
    },
    closePopupimport() {
      this.showPopupimport = false;
      this.file = null;
      this.importcontacts = [];
      this.duplicates = [];
    },
  },
};
</script>

<style scoped>
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

.tags-container {
  max-height: 120px;
  overflow-y: auto;
}
</style>
