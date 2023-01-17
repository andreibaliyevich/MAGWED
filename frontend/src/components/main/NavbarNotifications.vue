<template>
  <div class="navbar-notifications">
    <div class="dropdown">
      <a
        class="link-secondary position-relative"
        href="#"
        role="button"
        id="dropdownNotifications"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <i class="fa-solid fa-bell fa-lg"></i>
        <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle">
          <span class="visually-hidden">New notifications</span>
        </span>
      </a>
      <ul
        class="dropdown-menu dropdown-menu-end shadow w-100 overflow-auto"
        aria-labelledby="dropdownNotifications"
      >
        <li><a class="dropdown-item" href="#">Notifications 1</a></li>
        <li><a class="dropdown-item" href="#">Notifications 2</a></li>
        <li><a class="dropdown-item" href="#">Notifications 3</a></li>
        <li><a class="dropdown-item" href="#">Notifications 4</a></li>
        <li><a class="dropdown-item" href="#">Notifications 5 (Extended, Extended, Extended)</a></li>
        <li><a class="dropdown-item" href="#">Notifications 6</a></li>
        <li><a class="dropdown-item" href="#">Notifications 7</a></li>
        <li><a class="dropdown-item" href="#">Notifications 8</a></li>
      </ul>
    </div>
  </div>
</template>
