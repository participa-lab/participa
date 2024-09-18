const menu = () => {
  const btn = document.getElementById("menu-toggle");
  const nav = document.getElementById("nav");

  btn.addEventListener("click", () => {
    document.body.classList.toggle("menu-open");
    nav.classList.toggle("open");
    const expanded = btn.getAttribute("aria-expanded") === "true" || false;
    btn.setAttribute("aria-expanded", !expanded);
  });
};

export { menu };
