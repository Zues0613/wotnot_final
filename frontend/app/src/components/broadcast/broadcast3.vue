<template>
  <div class="p-4 sm:p-6">
    <!-- Section Header -->
    <div class="flex flex-col items-start justify-between gap-4 pb-5 mb-4 border-b md:flex-row md:items-center">
      <div>
        <h2 class="text-xl font-bold text-green-800 md:text-2xl">Scheduled Broadcasts</h2>
        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>
    </div>

    <!-- Broadcast List Table -->
    <h3 class="mb-4 text-xl text-green-800 md:text-2xs"><b>Scheduled Broadcast List</b></h3>

    <!-- Show empty state when no scheduled broadcasts -->
    <div v-if="broadcasts.length === 0" class="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <svg class="w-20 h-20 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
      </svg>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No Scheduled Broadcasts</h3>
      <p class="text-gray-500 mb-4 text-center">You haven't scheduled any broadcasts yet</p>
      <p class="text-sm text-gray-400 text-center">Schedule broadcasts from the Broadcast Messages tab to see them here</p>
    </div>

    <!-- Show table when scheduled broadcasts exist -->
    <div v-if="broadcasts.length > 0" class="overflow-x-auto max-h-[60vh] custom-scrollbar">
      <table class="w-full text-sm bg-white border border-gray-300 rounded-lg md:text-base">
        <thead>
          <tr class="font-semibold text-center text-gray-700 bg-gray-100">
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">ID</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Scheduled Time</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Broadcast Name</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Template</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Contacts</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Status</th>
            <th class="sticky top-0 z-10 p-3 text-center bg-gray-100 border border-gray-300 md:p-4">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="broadcast in broadcasts" :key="broadcast.id" class="hover:bg-gray-50">
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ broadcast.id }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ broadcast.scheduled_time }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ broadcast.name }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ broadcast.template }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">{{ broadcast.contacts.length }}</td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <div :class="{
                'bg-green-100 text-green-600 font-semibold px-2 py-1 rounded': broadcast.status === 'Successful',
                'bg-blue-100 text-blue-600 font-semibold px-2 py-1 rounded': broadcast.status === 'Scheduled',
                'bg-red-100 text-red-500 font-semibold px-2 py-1 rounded': broadcast.status === 'Cancelled',
                'bg-yellow-100 text-yellow-500 font-semibold px-2 py-1 rounded': broadcast.status === 'Partially Successful',
                'bg-yellow-100 text-yellow-600 font-semibold px-2 py-1 rounded': broadcast.status === 'pending...'
              }">
                {{ broadcast.status }}
              </div>
            </td>
            <td class="p-3 text-center border border-gray-200 md:p-4">
              <button @click="showDeleteConfirmation(broadcast.id)" class="p-2 transition rounded-full hover:bg-white">
                <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                  colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                </lord-icon>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <ConfirmationPopup v-if="showConfirmPopup" @yes="deleteScheduledBroadcast" @no="cancelDelete" @close="cancelDelete" message="Are you sure you want to delete this scheduled broadcast?"/>

  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import ConfirmationPopup from '../popups/confirmation'; // Assuming path is correct

export default {
  name: 'ScheduledBroadcasts',
  components: {
      ConfirmationPopup
  },
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      broadcasts: [],
      showConfirmPopup: false,
      broadcastIdToDelete: null,
    }
  },
  async mounted() {
    await this.fetchScheduledBroadcastList();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  methods: {
    async fetchScheduledBroadcastList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch(`${this.apiUrl}/scheduled-broadcast`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const scheduledBroadcastList = await response.json();
        this.broadcasts = scheduledBroadcastList.map(broadcast => ({
          id: broadcast.id,
          name: broadcast.name.split(' - ')[0],
          template: broadcast.template,
          contacts: broadcast.contacts,
          status: broadcast.status,
          scheduled_time: broadcast.scheduled_time
        }));
      } catch (error) {
        console.error('Error fetching scheduled-broadcastlist:', error);
      }
    },

    showDeleteConfirmation(broadcast_id) {
        this.broadcastIdToDelete = broadcast_id;
        this.showConfirmPopup = true;
    },

    cancelDelete() {
        this.showConfirmPopup = false;
        this.broadcastIdToDelete = null;
    },

    async deleteScheduledBroadcast() {
        if (!this.broadcastIdToDelete) return;

        const toast = useToast();
        const token = localStorage.getItem('token');
        
        try {
            const response = await fetch(`${this.apiUrl}/broadcasts-delete/${this.broadcastIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            } else {
                toast.success("Broadcast deleted successfully");
            }

            this.fetchScheduledBroadcastList(); // Refresh the list after deletion
        } catch (error) {
            console.error('Error deleting broadcast:', error);
            toast.error("Failed to delete the scheduled broadcast.");
        } finally {
            this.cancelDelete(); // Close popup and reset ID
        }
    },
  }
}
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
</style>
