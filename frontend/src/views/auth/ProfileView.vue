<script setup>
import { userType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'
import AdminProfileForm from '@/components/auth/AdminProfileForm.vue'
import CustomerProfileForm from '@/components/auth/CustomerProfileForm.vue'
import OrganizerProfileForm from '@/components/auth/OrganizerProfileForm.vue'

const userStore = useUserStore()
</script>

<template>
  <div class="profile-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">{{ $t('user.profile_settings') }}</h1>

      <ProfileCover v-if="userStore.userType === userType.ORGANIZER" />
      <ProfileAvatar />

      <AdminProfileForm v-if="userStore.userType === userType.ADMIN" />
      <CustomerProfileForm v-else-if="userStore.userType === userType.CUSTOMER" />
      <OrganizerProfileForm v-else-if="userStore.userType === userType.ORGANIZER" />
    </div>
  </div>
</template>
