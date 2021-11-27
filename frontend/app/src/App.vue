<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-layout>
      <n-layout-header>
        <n-image :src="logoUrl" alt="App logo" object-fit="contain" />
        <span>Toxic Comment Classification</span>
      </n-layout-header>

      <n-layout class="main-layout" has-sider>
        <n-layout-content content-style="padding: 5px;">
          <ChartTwoDim />
        </n-layout-content>

        <n-layout-sider content-style="padding: 5px 24px;">
          <Sidebar />
        </n-layout-sider>
      </n-layout>

      <n-layout-footer>
        <span>Made with ❤️</span>
      </n-layout-footer>
    </n-layout>
  </n-config-provider>
</template>

<script setup lang="ts">
  import {
    darkTheme,
    NConfigProvider,
    NLayout,
    NLayoutHeader,
    NLayoutFooter,
    NLayoutContent,
    NLayoutSider,
    NImage,
  } from 'naive-ui'
  import type { GlobalThemeOverrides } from 'naive-ui'
  import logoUrl from '@/assets/logo.png'
  import ChartTwoDim from '@/components/ChartTwoDim.vue'
  import Sidebar from '@/components/Sidebar.vue'

  const themeOverrides: GlobalThemeOverrides = {
    Button: {
      fontSizeLarge: '1.3rem',
    },
  }
</script>

<style lang="scss">
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
  }

  .main-layout {
    height: calc(100vh - 90px);
  }

  .n-layout-header {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: left;
    padding: 10px 30px;
    user-select: none;

    .n-image {
      aspect-ratio: 1;
      margin-right: 8px;
      // padding: 10px;
      // height: 40px;
      pointer-events: none;
    }

    span {
      font-size: 1.5rem;
      font-weight: 700;
    }
  }

  .n-layout-footer {
    // background: rgba(128, 128, 128, 0.2);
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: left;
    padding: 0 10px 0;
    user-select: none;
  }

  .n-layout-sider {
    --sider-width: 370px;
    max-width: var(--sider-width) !important;
    width: var(--sider-width) !important;
    background: rgba(27, 27, 27, 0.3);
    border-left: 1px solid rgb(49, 49, 49);
  }
</style>
