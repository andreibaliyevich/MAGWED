<script setup>
import { API_URL, userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const userStore = useUserStore()
</script>

<template>
  <div class="dropdown-user">
    <div class="dropdown ms-3">
      <a
        ref="dropdownUser"
        id="dropdownUser"
        href="#"
        class="d-flex align-items-center text-decoration-none text-decoration-none text-dark"
        data-bs-toggle="dropdown"
        data-bs-auto-close="outside"
        aria-expanded="false"
      >
        <img
          v-if="userStore.avatar"
          :src="`${ API_URL }${ userStore.avatar }`"
          class="rounded-circle"
          width="32"
          height="32"
          alt="avatar"
        >
        <img
          v-else
          src="/user-avatar.jpg"
          class="rounded-circle"
          width="32"
          height="32"
          alt="avatar"
        >
      </a>
      <ul
        class="dropdown-menu dropdown-menu-end shadow"
        aria-labelledby="dropdownUser"
      >
        <li class="px-3 pt-2 pb-3">
          <div class="d-flex gap-2 align-items-center mb-1">
            <img
              v-if="userStore.avatar"
              :src="`${ API_URL }${ userStore.avatar }`"
              class="rounded-circle"
              width="48"
              height="48"
              alt="avatar"
            >
            <img
              v-else
              src="/user-avatar.jpg"
              class="rounded-circle"
              width="48"
              height="48"
              alt="avatar"
            >
            <div class="ms-1">
              <span class="d-flex flex-nowrap fw-bolder">
                {{ userStore.name }}
              </span>
              <small class="text-muted">
                {{ userStore.email }}
              </small>
            </div>
          </div>
          <LocaleRouterLink
            routeName="Profile"
            @click="$refs.dropdownUser.click()"
            class="w-100 btn btn-light-brand btn-sm text-center"
          >
            {{ $t('auth.profile.edit_profile') }}
          </LocaleRouterLink>
        </li>
        <li>
          <LocaleRouterLink
            v-if="userStore.userType == userType.ORGANIZER"
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex gap-2 align-items-center"
          >
            <i class="fa-solid fa-users"></i>
            {{ $t('auth.followers') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex gap-2 align-items-center"
          >
            <i class="fa-solid fa-user-group"></i>
            {{ $t('auth.following') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex gap-2 align-items-center"
          >
            <i class="fa-solid fa-star"></i>
            {{ $t('auth.favorites') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex gap-2 align-items-center"
          >
            <i class="fa-solid fa-comment-dots"></i>
            {{ $t('footer.feedback') }}
          </LocaleRouterLink>
        </li>
        <li><hr class="dropdown-divider"></li>
        <li>
          <div
            @click="logout()"
            class="dropdown-item d-flex gap-2 align-items-center"
          >
            <i class="fa-solid fa-right-from-bracket"></i>
            {{ $t('auth.log_out') }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>