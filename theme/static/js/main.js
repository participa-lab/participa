import { menu } from "./menu.js";
import { slider } from "./slider.js";
import { Tabs } from "./tabs.js";

document.addEventListener("DOMContentLoaded", () => {
  menu();
  var splide = new Splide( '.splide' );
  splide.mount();
});
