var app = angular.module('customInterpolationApp', []);
 
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});