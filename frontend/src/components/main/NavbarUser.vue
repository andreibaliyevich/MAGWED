<script setup>
import { userType } from '@/config.js'
import { useLogout } from '@/composables/logout.js'
import { useUserStore } from '@/stores/user.js'

const { logout } = useLogout()
const userStore = useUserStore()
</script>

<template>
  <div class="navbar-user">
    <div class="dropdown">
      <a
        ref="dropdownUser"
        id="dropdownUser"
        href="#"
        class="text-decoration-none"
        data-bs-toggle="dropdown"
        data-bs-auto-close="outside"
        aria-expanded="false"
      >
        <UserAvatar
          :src="userStore.avatar"
          :width="32"
          :height="32"
          alt="avatar"
        />
      </a>
      <ul
        class="dropdown-menu dropdown-menu-end border border-light shadow"
        aria-labelledby="dropdownUser"
      >
        <li class="px-3 pt-2 pb-3">
          <div class="d-flex align-items-center gap-2 mb-1">
            <UserAvatar
              :src="userStore.avatar"
              :width="48"
              :height="48"
              alt="avatar"
            />
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
            class="btn btn-soft-brand btn-sm text-center w-100"
          >
            {{ $t('profile.edit_profile') }}
          </LocaleRouterLink>
        </li>
        <li>
          <LocaleRouterLink
            routeName="Messenger"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-message"></i>
            {{ $t('auth.messenger') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            v-if="userStore.userType == userType.ORGANIZER"
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-users"></i>
            {{ $t('auth.followers') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-user-group"></i>
            {{ $t('auth.following') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-star"></i>
            {{ $t('auth.favorites') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Home"
            @click="$refs.dropdownUser.click()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-comment-dots"></i>
            {{ $t('footer.feedback') }}
          </LocaleRouterLink>
        </li>
        <li><hr class="dropdown-divider"></li>
        <li>
          <div
            @click="logout()"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-right-from-bracket"></i>
            {{ $t('auth.log_out') }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
