/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
          colors: {
            'primary-2': 'rgba(0, 65, 70, 1)',
            'primary-1': 'rgba(0, 102, 109, 1)',
            'primary-regular': 'rgba(0, 139, 147, 1)',
            'secondary-regular': 'rgba(226, 86, 34, 1)',
            'secondary-white': 'rgba(255, 255, 255, 1)',
            'danger-1': 'rgba(169, 0, 0, 1)',
            'danger-regular': 'rgba(227, 24, 24, 1)',
            naranja: '#e25622',
            turquesa: '#00808c',
          },
          fontFamily: {
            'libre-franklin': ['"Libre Franklin"', 'Helvetica', 'sans-serif'],
          },
          boxShadow: {
            'cards-style': '6px 6px 14px 0px rgba(0, 0, 0, 0.05)',
          },
          letterSpacing: {
            '-1.92px': '-1.92px',
            '2px': '2px',
          },
          lineHeight: {
            '94.4px': '94.4px',
            '150%': '1.5',
          },
          fontSize: {
            '96px': '96px',
            '40px': '40px',
            '24px': '24px',
            '20px': '20px',
            '18px': '18px',
            '16px': '16px',
            '14px': '14px',
          },
        },
      },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
