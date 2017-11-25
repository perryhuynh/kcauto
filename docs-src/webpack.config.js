const path = require('path');
const webpack = require('webpack');
const srcPath = path.join(__dirname, 'src');
const modulesPath = path.join(__dirname, '..', 'node_modules');
const outputPath = path.join(__dirname, '..', 'docs');

module.exports = env => {
  const isProd = env.prod;
  const isDev = env.dev;
  const pluginsArray = [];
  if (isProd) {
    pluginsArray.push(new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }))
    pluginsArray.push(new webpack.optimize.UglifyJsPlugin());
}

  return {
    entry: srcPath + '/index.jsx',
    output: {
      path: outputPath,
      filename: 'bundle.js',
      sourceMapFilename: '[file].map?[contenthash]'
    },
    plugins: pluginsArray,
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          include: [srcPath],
          use: [
            {
              loader: 'babel-loader',
              options: {
                presets: ['env', 'react', 'stage-0']
              }
            }
          ]
        },
        {
          test: /\.css$/,
          include: [modulesPath],
          use: [
            {
              loader: 'style-loader'
            },
            {
              loader: 'css-loader',
              options: {
                'sourceMap': true
              }
            }
          ]
        },
      ]
    },
    resolve: {
      modules: [srcPath, modulesPath],
      extensions: ['.js', '.jsx', '.css']
    },
    devtool: 'source-map'
  }
};
