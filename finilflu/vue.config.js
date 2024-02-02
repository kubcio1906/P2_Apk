module.exports = {
  chainWebpack: (config) => {
    config.plugin('feature-flags').tap((args) => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = false;
      return args;
    });
  }
};