const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true),
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
      }),
    ],
  },
  chainWebpack: config => {
    // Register lord-icon as custom element to suppress warnings
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap(options => ({
        ...options,
        compilerOptions: {
          isCustomElement: tag => tag === 'lord-icon'
        }
      }));
  },
  devServer: {
    allowedHosts: 'all',  // Disable host checking
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000', // Load from .env
        changeOrigin: true,
        secure: false,
      },
    },
    // WebSocket configuration for hot reload (automatically uses local)
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws', // Auto-detect local WebSocket
    },
  },
};
