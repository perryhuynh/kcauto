const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const srcPath = path.join(__dirname, 'src');
const modulesPath = path.join(__dirname, '..', 'node_modules');
const outputPath = path.join(__dirname, '..', 'docs');

module.exports = env => {
  const pluginsArray = [new webpack.DefinePlugin({
    'process.version': JSON.stringify(process.env.npm_package_version),
  })];

  const config = {
    entry: srcPath + '/index.jsx',
    output: {
      path: outputPath,
      filename: 'bundle.js'
    },
    plugins: pluginsArray,
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          include: [srcPath],
          use: ['babel-loader']
        },
        {
          test: /\.css$/,
          include: [modulesPath],
          use: [
            'style-loader',
            'css-loader'
          ]
        }
      ]
    },
    resolve: {
      modules: [srcPath, modulesPath],
      extensions: ['.js', '.jsx', '.css']
    },
  }

  if (env.NODE_ENV === 'production') {
    config.optimization = {
      minimizer: [
        new UglifyJsPlugin({
          parallel: true,
          sourceMap: false,
        })
      ]
    }
  } else {
    config.output.sourceMapFilename = '[file].map?[contenthash]'
    config.devtool = 'source-map'
  }

  return config
};
