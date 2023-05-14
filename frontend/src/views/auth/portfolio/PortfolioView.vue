
<template>
  <div class="portfolio-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.portfolio.portfolio') }}
      </h1>

      <div class="bg-light rounded-3 p-5">
        <h2>{{ $t('auth.portfolio.albums') }}</h2>
        <p></p>
        <LocaleRouterLink
          routeName="PortfolioAlbumList"
          class="btn btn-soft-brand"
        >
          {{ $t('auth.portfolio.view_albums') }}
        </LocaleRouterLink>
      </div>

      <div class="bg-light rounded-3 p-5 mt-2">
        <h2>{{ $t('auth.portfolio.photos') }}</h2>
        <p></p>
        <LocaleRouterLink
          routeName="PortfolioPhotoList"
          class="btn btn-soft-brand"
        >
          {{ $t('auth.portfolio.view_photos') }}
        </LocaleRouterLink>
      </div>

    </div>
  </div>
</template>
