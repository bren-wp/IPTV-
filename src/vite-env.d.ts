/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_IPTV_EDITION?: 'free' | 'pro';
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
