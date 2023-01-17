<template>
  <div class="navbar-search">
    <div class="dropdown mt-3 mt-lg-0">
      <form
        class="d-flex align-items-center border rounded-pill"
        id="dropdownSearch"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <span class="text-secondary ms-2">
          <i class="fa-solid fa-magnifying-glass"></i>
        </span>
        <input
          class="form-control rounded-pill border-0 shadow-none m-1"
          id="search"
          type="search"
          placeholder="Search..."
          aria-label="Search"
          autocomplete="off"
        >
      </form>
      <ul
        class="dropdown-menu shadow w-100 overflow-auto"
        aria-labelledby="dropdownSearch"
      >
        <li><a class="dropdown-item" href="#">Search Result 1</a></li>
        <li><a class="dropdown-item" href="#">Search Result 2</a></li>
        <li><a class="dropdown-item" href="#">Search Result 3</a></li>
        <li><a class="dropdown-item" href="#">Search Result 4</a></li>
        <li><a class="dropdown-item" href="#">Search Result 5 (Extended, Extended, Extended)</a></li>
        <li><a class="dropdown-item" href="#">Search Result 6</a></li>
        <li><a class="dropdown-item" href="#">Search Result 7</a></li>
        <li><a class="dropdown-item" href="#">Search Result 8</a></li>
      </ul>
    </div>
  </div>
</template>
