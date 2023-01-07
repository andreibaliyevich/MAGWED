<script setup>
import { userType } from '@/config.js'

import { useUserStore } from '@/stores/user.js'
const user = useUserStore()

import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'
import AdminProfileForm from '@/components/auth/AdminProfileForm.vue'
import CustomerProfileForm from '@/components/auth/CustomerProfileForm.vue'
import OrganizerProfileForm from '@/components/auth/OrganizerProfileForm.vue'
</script>

<template>
  <div class="profile-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">{{ $t('auth.profile.profile_settings') }}</h1>

      <ProfileCover v-if="user.userType == userType.ORGANIZER" />
      <ProfileAvatar />

      <AdminProfileForm v-if="user.userType == userType.ADMIN" />
      <CustomerProfileForm v-else-if="user.userType == userType.CUSTOMER" />
      <OrganizerProfileForm v-else-if="user.userType == userType.ORGANIZER" />
    </div>
  </div>
</template>
