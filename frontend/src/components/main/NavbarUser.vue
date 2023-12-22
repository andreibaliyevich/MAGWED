<script setup>
import { userType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useLogout } from '@/composables/logout.js'

const userStore = useUserStore()
const { logout } = useLogout()
</script>

<template>
  <div class="navbar-user">
    <div class="dropdown">
      <button
        id="user_dropdown"
        type="button"
        class="btn btn-link p-0"
        data-bs-toggle="dropdown"
        data-bs-auto-close="true"
        aria-expanded="false"
      >
        <UserAvatar
          :src="userStore.avatar"
          :width="32"
          :height="32"
          alt="avatar"
        />
      </button>
      <ul
        class="dropdown-menu dropdown-menu-end border border-light shadow"
        aria-labelledby="user_dropdown"
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
            class="btn btn-soft-brand btn-sm text-center w-100"
          >
            {{ $t('user.edit_profile') }}
          </LocaleRouterLink>
        </li>
        <li>
          <LocaleRouterLink
            routeName="Messenger"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-message"></i>
            {{ $t('messenger.messenger') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            v-if="userStore.userType == userType.ORGANIZER"
            routeName="Followers"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-users"></i>
            {{ $t('follow.followers') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Following"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-user-group"></i>
            {{ $t('follow.following') }}
          </LocaleRouterLink>
          <LocaleRouterLink
            routeName="Favorites"
            class="dropdown-item d-flex align-items-center gap-2"
          >
            <i class="fa-solid fa-star"></i>
            {{ $t('favorites.favorites') }}
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
