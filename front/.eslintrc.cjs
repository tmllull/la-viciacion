module.exports = {
    env: {
        es6: true,
        browser: true,
        node: true,
        jest: true,
    },
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        ecmaFeatures: {
            jsx: true,
            experimentalObjectRestSpread: true,
            generators: false,
            objectLiteralDuplicateProperties: false,
            legacyDecotators: true,
        },
    },
    plugins: [
        'react',
        'import',
        'jsx-a11y',
    ],
    globals: {
        Cypress: 'readonly',
        cy: 'readonly',
        describe: 'readonly',
    },
    settings: {
        'import/resolver': {
            node: {
                extensions: ['.mjs', '.js', '.json', '.jsx'],
                paths: ['src'],
                moduleDirectory: ["node_modules", "src/"]
            },
        },
        'import/extensions': [
            '.js',
            '.mjs',
            '.jsx',
        ],
        'import/core-modules': [],
        'import/ignore': [
            'node_modules',
            '\\.(coffee|scss|css|less|hbs|svg|json)$',
        ],
        react: {
            pragma: 'React',
            version: 'detect',
        },
        propWrapperFunctions: [
            'forbidExtraProps', // https://www.npmjs.com/package/airbnb-prop-types
            'exact', // https://www.npmjs.com/package/prop-types-exact
            'Object.freeze', // https://tc39.github.io/ecma262///sec-object.freeze
        ],
    },
    rules: {
        // NOTE -------------------------------- NODE -------------------------------->>>>>>>>>>>>>
        // enforce return after a callback
        'callback-return': 'off',

        // require all requires be top-level
        // https://eslint.org/docs/rules/global-require
        'global-require': 'error',

        // enforces error handling in callbacks (node environment)
        'handle-callback-err': 'off',

        // disallow use of the Buffer() constructor
        // https://eslint.org/docs/rules/no-buffer-constructor
        'no-buffer-constructor': 'error',

        // disallow mixing regular variable and require declarations
        'no-mixed-requires': ['off', false],

        // disallow use of new operator with the require function
        'no-new-require': 'error',

        // disallow string concatenation with __dirname and __filename
        // https://eslint.org/docs/rules/no-path-concat
        'no-path-concat': 'error',

        // disallow use of process.env
        'no-process-env': 'off',

        // disallow process.exit()
        'no-process-exit': 'off',

        // restrict usage of specified node modules
        'no-restricted-modules': 'off',

        // disallow use of synchronous methods (off by default)
        'no-sync': 'off',
        // NOTE -------------------------------- ES6 -------------------------------->>>>>>>>>>>>>
        // enforces no braces where they can be omitted
        // https://eslint.org/docs/rules/arrow-body-style
        // TODO: enable requireReturnForObjectLiteral?
        'arrow-body-style': ['warn', 'as-needed', {
            requireReturnForObjectLiteral: false,
        }],

        // require parens in arrow function arguments
        // https://eslint.org/docs/rules/arrow-parens
        'arrow-parens': ['error', 'as-needed', {
            requireForBlockBody: true,
        }],

        // require space before/after arrow function"s arrow
        // https://eslint.org/docs/rules/arrow-spacing
        'arrow-spacing': ['error', { before: true, after: true }],

        // verify super() callings in constructors
        'constructor-super': 'error',

        // enforce the spacing around the * in generator functions
        // https://eslint.org/docs/rules/generator-star-spacing
        'generator-star-spacing': ['error', { before: false, after: true }],

        // disallow modifying variables of class declarations
        // https://eslint.org/docs/rules/no-class-assign
        'no-class-assign': 'error',

        // disallow arrow functions where they could be confused with comparisons
        // https://eslint.org/docs/rules/no-confusing-arrow
        'no-confusing-arrow': ['error', {
            allowParens: true,
        }],

        // disallow modifying variables that are declared using const
        'no-const-assign': 'error',

        // disallow duplicate class members
        // https://eslint.org/docs/rules/no-dupe-class-members
        'no-dupe-class-members': 'error',

        // disallow importing from the same path more than once
        // https://eslint.org/docs/rules/no-duplicate-imports
        // replaced by https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-duplicates.md
        'no-duplicate-imports': 'off',

        // disallow symbol constructor
        // https://eslint.org/docs/rules/no-new-symbol
        'no-new-symbol': 'error',

        // disallow specific imports
        // https://eslint.org/docs/rules/no-restricted-imports
        'no-restricted-imports': ['off', {
            paths: [],
            patterns: [],
        }],

        // disallow to use this/super before super() calling in constructors.
        // https://eslint.org/docs/rules/no-this-before-super
        'no-this-before-super': 'error',

        // disallow useless computed property keys
        // https://eslint.org/docs/rules/no-useless-computed-key
        'no-useless-computed-key': 'error',

        // disallow unnecessary constructor
        // https://eslint.org/docs/rules/no-useless-constructor
        'no-useless-constructor': 'error',

        // disallow renaming import, export, and destructured assignments to the same name
        // https://eslint.org/docs/rules/no-useless-rename
        'no-useless-rename': ['error', {
            ignoreDestructuring: false,
            ignoreImport: false,
            ignoreExport: false,
        }],

        // require let or const instead of var
        'no-var': 'error',

        // require method and property shorthand syntax for object literals
        // https://eslint.org/docs/rules/object-shorthand
        'object-shorthand': ['error', 'always', {
            ignoreConstructors: false,
            avoidQuotes: true,
        }],

        // suggest using arrow functions as callbacks
        'prefer-arrow-callback': ['error', {
            allowNamedFunctions: false,
            allowUnboundThis: true,
        }],

        // suggest using of const declaration for variables that are never modified after declared
        'prefer-const': ['error', {
            destructuring: 'any',
            ignoreReadBeforeAssign: true,
        }],

        // Prefer destructuring from arrays and objects
        // https://eslint.org/docs/rules/prefer-destructuring
        'prefer-destructuring': ['error', {
            VariableDeclarator: {
                array: false,
                object: true,
            },
            AssignmentExpression: {
                array: true,
                object: true,
            },
        }, {
            enforceForRenamedProperties: false,
        }],

        // disallow parseInt() in favor of binary, octal, and hexadecimal literals
        // https://eslint.org/docs/rules/prefer-numeric-literals
        'prefer-numeric-literals': 'error',

        // suggest using Reflect methods where applicable
        // https://eslint.org/docs/rules/prefer-reflect
        'prefer-reflect': 'off',

        // use rest parameters instead of arguments
        // https://eslint.org/docs/rules/prefer-rest-params
        'prefer-rest-params': 'error',

        // suggest using the spread operator instead of .apply()
        // https://eslint.org/docs/rules/prefer-spread
        'prefer-spread': 'error',

        // suggest using template literals instead of string concatenation
        // https://eslint.org/docs/rules/prefer-template
        'prefer-template': 'error',

        // disallow generator functions that do not have yield
        // https://eslint.org/docs/rules/require-yield
        'require-yield': 'error',

        // enforce spacing between object rest-spread
        // https://eslint.org/docs/rules/rest-spread-spacing
        'rest-spread-spacing': ['error', 'never'],

        // import sorting
        // https://eslint.org/docs/rules/sort-imports
        'sort-imports': ['off', {
            ignoreCase: false,
            ignoreMemberSort: false,
            memberSyntaxSortOrder: ['none', 'all', 'multiple', 'single'],
        }],

        // require a Symbol description
        // https://eslint.org/docs/rules/symbol-description
        'symbol-description': 'error',

        // enforce usage of spacing in template strings
        // https://eslint.org/docs/rules/template-curly-spacing
        'template-curly-spacing': 'error',

        // enforce spacing around the * in yield* expressions
        // https://eslint.org/docs/rules/yield-star-spacing
        'yield-star-spacing': ['error', 'after'],

        // //NOTE ---------------- best-practices ----------------

        // enforces getter/setter pairs in objects
        'accessor-pairs': 'off',

        // enforces return statements in callbacks of array"s methods
        // https://eslint.org/docs/rules/array-callback-return
        'array-callback-return': ['error', { allowImplicit: true }],

        // treat var statements as if they were block scoped
        'block-scoped-var': 'error',

        // specify the maximum cyclomatic complexity allowed in a program
        complexity: ['off', 11],

        // //enforce that class methods use "this"
        // //https://eslint.org/docs/rules/class-methods-use-this
        // "class-methods-use-this": ["error", {
        //    "exceptMethods": []
        // }],

        // require return statements to either always or never specify values
        'consistent-return': 'error',

        // specify curly brace conventions for all control statements
        curly: ['error', 'multi-line'],

        // require default case in switch statements
        'default-case': ['error', { commentPattern: '^no default$' }],

        // encourages use of dot notation whenever possible
        'dot-notation': ['error', { allowKeywords: true }],

        // enforces consistent newlines before or after dots
        // https://eslint.org/docs/rules/dot-location
        'dot-location': ['error', 'property'],

        // require the use of === and !==
        // https://eslint.org/docs/rules/eqeqeq
        eqeqeq: ['error', 'always', { null: 'ignore' }],

        // make sure for-in loops have an if statement
        'guard-for-in': 'error',

        // disallow the use of alert, confirm, and prompt
        'no-alert': 'warn',

        // disallow use of arguments.caller or arguments.callee
        'no-caller': 'error',

        // disallow lexical declarations in case/default clauses
        // https://eslint.org/docs/rules/no-case-declarations.html
        'no-case-declarations': 'error',

        // disallow division operators explicitly at beginning of regular expression
        // https://eslint.org/docs/rules/no-div-regex
        'no-div-regex': 'off',

        // disallow else after a return in an if
        // https://eslint.org/docs/rules/no-else-return
        'no-else-return': ['error', { allowElseIf: false }],

        // disallow empty functions, except for standalone funcs/arrows
        // https://eslint.org/docs/rules/no-empty-function
        'no-empty-function': ['error', {
            allow: [
                'arrowFunctions',
                'functions',
                'methods',
            ],
        }],

        // disallow empty destructuring patterns
        // https://eslint.org/docs/rules/no-empty-pattern
        'no-empty-pattern': 'error',

        // disallow comparisons to null without a type-checking operator
        'no-eq-null': 'off',

        // disallow use of eval()
        'no-eval': 'error',

        // disallow adding to native types
        'no-extend-native': 'error',

        // disallow unnecessary function binding
        'no-extra-bind': 'error',

        // disallow Unnecessary Labels
        // https://eslint.org/docs/rules/no-extra-label
        'no-extra-label': 'error',

        // disallow fallthrough of case statements
        'no-fallthrough': 'error',

        // disallow the use of leading or trailing decimal points in numeric literals
        'no-floating-decimal': 'error',

        // disallow reassignments of native objects or read-only globals
        // https://eslint.org/docs/rules/no-global-assign
        'no-global-assign': ['error', { exceptions: [] }],
        // deprecated in favor of no-global-assign
        'no-native-reassign': 'off',

        // disallow implicit type conversions
        // https://eslint.org/docs/rules/no-implicit-coercion
        'no-implicit-coercion': ['off', {
            boolean: false,
            number: true,
            string: true,
            allow: [],
        }],

        // disallow var and named functions in global scope
        // https://eslint.org/docs/rules/no-implicit-globals
        'no-implicit-globals': 'off',

        // disallow use of eval()-like methods
        'no-implied-eval': 'error',

        // disallow this keywords outside of classes or class-like objects
        'no-invalid-this': 'off',

        // disallow usage of __iterator__ property
        'no-iterator': 'error',

        // disallow use of labels for anything other then loops and switches
        'no-labels': ['error', { allowLoop: false, allowSwitch: false }],

        // disallow unnecessary nested blocks
        'no-lone-blocks': 'error',

        // disallow creation of functions within loops
        'no-loop-func': 'error',

        // disallow magic numbers
        // https://eslint.org/docs/rules/no-magic-numbers
        'no-magic-numbers': ['off', {
            ignore: [],
            ignoreArrayIndexes: true,
            enforceConst: true,
            detectObjects: false,
        }],

        // disallow use of multiple spaces
        'no-multi-spaces': ['error', {
            ignoreEOLComments: false,
        }],

        // disallow use of multiline strings
        'no-multi-str': 'error',

        // disallow use of new operator when not part of the assignment or comparison
        'no-new': 'error',

        // disallow use of new operator for Function object
        'no-new-func': 'error',

        // disallows creating new instances of String, Number, and Boolean
        'no-new-wrappers': 'error',

        // disallow use of (old style) octal literals
        'no-octal': 'error',

        // disallow use of octal escape sequences in string literals, such as
        // var foo = "Copyright \251";
        'no-octal-escape': 'error',

        // disallow reassignment of function parameters
        // disallow parameter object manipulation except for specific exclusions
        // rule: https://eslint.org/docs/rules/no-param-reassign.html
        'no-param-reassign': ['error', {
            props: false,
            // "ignorePropertyModificationsFor": [
            //    "acc", //for reduce accumulators
            //    "accumulator", //for reduce accumulators
            //    "e", //for e.returnvalue
            //    "ctx", //for Koa routing
            //    "req", //for Express requests
            //    "request", //for Express requests
            //    "res", //for Express responses
            //    "response", //for Express responses
            //    "$scope" //for Angular 1 scopes
            // ]
        }],

        // disallow usage of __proto__ property
        'no-proto': 'error',

        // disallow declaring the same variable more then once
        'no-redeclare': 'error',

        // disallow certain object properties
        // https://eslint.org/docs/rules/no-restricted-properties
        'no-restricted-properties': ['error', {
            object: 'arguments',
            property: 'callee',
            message: 'arguments.callee is deprecated',
        }, {
            object: 'global',
            property: 'isFinite',
            message: 'Please use Number.isFinite instead',
        }, {
            object: 'self',
            property: 'isFinite',
            message: 'Please use Number.isFinite instead',
        }, {
            object: 'window',
            property: 'isFinite',
            message: 'Please use Number.isFinite instead',
        }, {
            object: 'global',
            property: 'isNaN',
            message: 'Please use Number.isNaN instead',
        }, {
            object: 'self',
            property: 'isNaN',
            message: 'Please use Number.isNaN instead',
        }, {
            object: 'window',
            property: 'isNaN',
            message: 'Please use Number.isNaN instead',
        }, {
            property: '__defineGetter__',
            message: 'Please use Object.defineProperty instead.',
        }, {
            property: '__defineSetter__',
            message: 'Please use Object.defineProperty instead.',
        }, {
            object: 'Math',
            property: 'pow',
            message: 'Use the exponentiation operator (**) instead.',
        },
        ],

        // disallow use of assignment in return statement
        'no-return-assign': ['error', 'always'],

        // disallow redundant `return await`
        'no-return-await': 'error',

        // disallow use of `javascript:` urls.
        'no-script-url': 'error',

        // disallow self assignment
        // https://eslint.org/docs/rules/no-self-assign
        'no-self-assign': 'error',

        // disallow comparisons where both sides are exactly the same
        'no-self-compare': 'error',

        // disallow use of comma operator
        'no-sequences': 'error',

        // restrict what can be thrown as an exception
        'no-throw-literal': 'error',

        // disallow unmodified conditions of loops
        // https://eslint.org/docs/rules/no-unmodified-loop-condition
        'no-unmodified-loop-condition': 'off',

        // disallow usage of expressions in statement position
        'no-unused-expressions': ['error', {
            allowShortCircuit: false,
            allowTernary: false,
            allowTaggedTemplates: false,
        }],

        // disallow unused labels
        // https://eslint.org/docs/rules/no-unused-labels
        'no-unused-labels': 'error',

        // disallow unnecessary .call() and .apply()
        'no-useless-call': 'off',

        // disallow useless string concatenation
        // https://eslint.org/docs/rules/no-useless-concat
        'no-useless-concat': 'error',

        // disallow unnecessary string escaping
        // https://eslint.org/docs/rules/no-useless-escape
        'no-useless-escape': 'error',

        // disallow redundant return; keywords
        // https://eslint.org/docs/rules/no-useless-return
        'no-useless-return': 'error',

        // disallow use of void operator
        // https://eslint.org/docs/rules/no-void
        'no-void': 'error',

        // disallow usage of configurable warning terms in comments: e.g. todo
        'no-warning-comments': ['off', { terms: ['todo', 'fixme', 'xxx'], location: 'start' }],

        // disallow use of the with statement
        'no-with': 'error',

        // require using Error objects as Promise rejection reasons
        // https://eslint.org/docs/rules/prefer-promise-reject-errors
        'prefer-promise-reject-errors': ['error', { allowEmptyReject: true }],

        // require use of the second argument for parseInt()
        radix: 'error',

        // require `await` in `async function` (note: this is a horrible rule that should never be used)
        // https://eslint.org/docs/rules/require-await
        'require-await': 'off',

        // requires to declare all vars on top of their containing scope
        'vars-on-top': 'error',

        // require immediate function invocation to be wrapped in parentheses
        // https://eslint.org/docs/rules/wrap-iife.html
        'wrap-iife': ['error', 'outside', { functionPrototypeMethods: false }],

        // require or disallow Yoda conditions
        yoda: 'error',

        // NOTE -------------------------------- style -------------------------------->>>>>>>>>>>>>
        // enforce line breaks after opening and before closing array brackets
        // https://eslint.org/docs/rules/array-bracket-newline
        // TODO: enable? semver-major
        'array-bracket-newline': ['off', 'consistent'], // object option alternative: { multiline: true, minItems: 3 }

        // enforce line breaks between array elements
        // https://eslint.org/docs/rules/array-element-newline
        // TODO: enable? semver-major
        'array-element-newline': ['off', { multiline: true, minItems: 3 }],

        // enforce spacing inside array brackets
        'array-bracket-spacing': ['error', 'never'],

        // enforce spacing inside single-line blocks
        // https://eslint.org/docs/rules/block-spacing
        'block-spacing': ['error', 'always'],

        // enforce one true brace style
        'brace-style': ['error', '1tbs', { allowSingleLine: true }],

        // require camel case names
        camelcase: ['error', { properties: 'never' }],

        // enforce or disallow capitalization of the first letter of a comment
        // https://eslint.org/docs/rules/capitalized-comments
        'capitalized-comments': ['off', 'never', {
            line: {
                ignorePattern: '.*',
                ignoreInlineComments: true,
                ignoreConsecutiveComments: true,
            },
            block: {
                ignorePattern: '.*',
                ignoreInlineComments: true,
                ignoreConsecutiveComments: true,
            },
        }],

        // require trailing commas in multiline object literals
        'comma-dangle': ['error', {
            arrays: 'always-multiline',
            objects: 'always-multiline',
            imports: 'always-multiline',
            exports: 'always-multiline',
            functions: 'always-multiline',
        }],

        // enforce spacing before and after comma
        'comma-spacing': ['error', { before: false, after: true }],

        // enforce one true comma style
        'comma-style': ['error', 'last', {
            exceptions: {
                ArrayExpression: false,
                ArrayPattern: false,
                ArrowFunctionExpression: false,
                CallExpression: false,
                FunctionDeclaration: false,
                FunctionExpression: false,
                ImportDeclaration: false,
                ObjectExpression: false,
                ObjectPattern: false,
                VariableDeclaration: false,
                NewExpression: false,
            },
        }],

        // disallow padding inside computed properties
        'computed-property-spacing': ['error', 'never'],

        // enforces consistent naming when capturing the current execution context
        'consistent-this': 'off',

        // enforce newline at the end of file, with no multiple empty lines
        'eol-last': ['error', 'always'],

        // enforce spacing between functions and their invocations
        // https://eslint.org/docs/rules/func-call-spacing
        'func-call-spacing': ['error', 'never'],

        // requires function names to match the name of the variable or property to which they are
        // assigned
        // https://eslint.org/docs/rules/func-name-matching
        'func-name-matching': ['off', 'always', {
            includeCommonJSModuleExports: false,
        }],

        // require function expressions to have a name
        // https://eslint.org/docs/rules/func-names
        'func-names': 'warn',

        // enforces use of function declarations or expressions
        // https://eslint.org/docs/rules/func-style
        // TODO: enable
        'func-style': ['off', 'expression'],

        // enforce consistent line breaks inside function parentheses
        // https://eslint.org/docs/rules/function-paren-newline
        'function-paren-newline': ['error', 'consistent'],

        // Blacklist certain identifiers to prevent them being used
        // https://eslint.org/docs/rules/id-blacklist
        'id-blacklist': 'off',

        // this option enforces minimum and maximum identifier lengths
        // (variable names, property names etc.)
        'id-length': 'off',

        // require identifiers to match the provided regular expression
        'id-match': 'off',

        // Enforce the location of arrow function bodies with implicit returns
        // https://eslint.org/docs/rules/implicit-arrow-linebreak
        'implicit-arrow-linebreak': ['error', 'beside'],

        // this option sets a specific tab width for your code
        // https://eslint.org/docs/rules/indent
        indent: ['error', 4, {
            SwitchCase: 1,
            VariableDeclarator: 1,
            outerIIFEBody: 1,
            // "MemberExpression": null,
            FunctionDeclaration: {
                parameters: 1,
                body: 1,
            },
            FunctionExpression: {
                parameters: 1,
                body: 1,
            },
            CallExpression: {
                arguments: 1,
            },
            ArrayExpression: 1,
            ObjectExpression: 1,
            ImportDeclaration: 1,
            flatTernaryExpressions: false,
            // list derived from https://github.com/benjamn/ast-types/blob/HEAD/def/jsx.js
            ignoredNodes: ['JSXElement', 'JSXElement > *', 'JSXAttribute', 'JSXIdentifier', 'JSXNamespacedName', 'JSXMemberExpression', 'JSXSpreadAttribute', 'JSXExpressionContainer', 'JSXOpeningElement', 'JSXClosingElement', 'JSXText', 'JSXEmptyExpression', 'JSXSpreadChild'],
            ignoreComments: false,
        }],

        // specify whether double or single quotes should be used in JSX attributes
        // https://eslint.org/docs/rules/jsx-quotes
        // "jsx-quotes": ["off", "prefer-single"],

        // enforces spacing between keys and values in object literal properties
        'key-spacing': ['error', { beforeColon: false, afterColon: true }],

        // require a space before & after certain keywords
        'keyword-spacing': ['error', {
            before: true,
            after: true,
            overrides: {
                return: { after: true },
                throw: { after: true },
                case: { after: true },
            },
        }],

        // enforce position of line comments
        // https://eslint.org/docs/rules/line-comment-position
        // TODO: enable?
        'line-comment-position': ['off', {
            position: 'above',
            ignorePattern: '',
            applyDefaultPatterns: true,
        }],

        // disallow mixed "LF" and "CRLF" as linebreaks
        // https://eslint.org/docs/rules/linebreak-style
        // "linebreak-style": ["error", "unix"], //

        // require or disallow an empty line between class members
        // https://eslint.org/docs/rules/lines-between-class-members
        'lines-between-class-members': ['error', 'always', { exceptAfterSingleLine: false }],

        // enforces empty lines around comments
        'lines-around-comment': 'off',

        // require or disallow newlines around directives
        // https://eslint.org/docs/rules/lines-around-directive
        'lines-around-directive': ['error', {
            before: 'always',
            after: 'always',
        }],

        // specify the maximum depth that blocks can be nested
        'max-depth': ['off', 4],

        // specify the maximum length of a line in your program
        // https://eslint.org/docs/rules/max-len
        'max-len': ['error', 200, 2, {
            ignoreUrls: true,
            ignoreComments: true,
            ignoreRegExpLiterals: true,
            ignoreStrings: true,
            ignoreTemplateLiterals: true,
        }],

        // specify the max number of lines in a file
        // https://eslint.org/docs/rules/max-lines
        'max-lines': ['off', {
            max: 300,
            skipBlankLines: true,
            skipComments: true,
        }],

        // specify the maximum depth callbacks can be nested
        'max-nested-callbacks': 'off',

        // limits the number of parameters that can be used in the function declaration.
        'max-params': ['off', 3],

        // specify the maximum number of statement allowed in a function
        'max-statements': ['off', 10],

        // restrict the number of statements per line
        // https://eslint.org/docs/rules/max-statements-per-line
        'max-statements-per-line': ['off', { max: 1 }],

        // enforce a particular style for multiline comments
        // https://eslint.org/docs/rules/multiline-comment-style
        'multiline-comment-style': ['off', 'starred-block'],

        // require multiline ternary
        // https://eslint.org/docs/rules/multiline-ternary
        // TODO: enable?
        'multiline-ternary': ['off', 'never'],

        // require a capital letter for constructors
        'new-cap': ['error', {
            newIsCap: true,
            newIsCapExceptions: [],
            capIsNew: false,
            capIsNewExceptions: ['Immutable.Map', 'Immutable.Set', 'Immutable.List'],
        }],

        // disallow the omission of parentheses when invoking a constructor with no arguments
        // https://eslint.org/docs/rules/new-parens
        'new-parens': 'error',

        // allow/disallow an empty newline after var statement
        'newline-after-var': 'off',

        // https://eslint.org/docs/rules/newline-before-return
        'newline-before-return': 'off',

        // enforces new line after each method call in the chain to make it
        // more readable and easy to maintain
        // https://eslint.org/docs/rules/newline-per-chained-call
        'newline-per-chained-call': ['error', { ignoreChainWithDepth: 4 }],

        // disallow use of the Array constructor
        'no-array-constructor': 'error',

        // disallow use of bitwise operators
        // https://eslint.org/docs/rules/no-bitwise
        'no-bitwise': 'error',

        // disallow use of the continue statement
        // https://eslint.org/docs/rules/no-continue
        'no-continue': 'error',

        // disallow comments inline after code
        'no-inline-comments': 'off',

        // disallow if as the only statement in an else block
        // https://eslint.org/docs/rules/no-lonely-if
        'no-lonely-if': 'error',

        // disallow un-paren"d mixes of different operators
        // https://eslint.org/docs/rules/no-mixed-operators
        'no-mixed-operators': ['error', {
            // the list of arthmetic groups disallows mixing `%` and `**`
            // with other arithmetic operators.
            groups: [
                ['%', '**'],
                ['%', '+'],
                ['%', '-'],
                ['%', '*'],
                ['%', '/'],
                ['**', '+'],
                ['**', '-'],
                ['**', '*'],
                ['**', '/'],
                ['&', '|', '^', '~', '<<', '>>', '>>>'],
                ['==', '!=', '===', '!==', '>', '>=', '<', '<='],
                ['&&', '||'],
                ['in', 'instanceof'],
            ],
            allowSamePrecedence: false,
        }],

        // disallow mixed spaces and tabs for indentation
        'no-mixed-spaces-and-tabs': 'error',

        // disallow use of chained assignment expressions
        // https://eslint.org/docs/rules/no-multi-assign
        'no-multi-assign': ['error'],

        // disallow multiple empty lines and only one newline at the end
        'no-multiple-empty-lines': ['error', { max: 2, maxEOF: 0 }],

        // disallow negated conditions
        // https://eslint.org/docs/rules/no-negated-condition
        'no-negated-condition': 'off',

        // disallow nested ternary expressions
        'no-nested-ternary': 'error',

        // disallow use of the Object constructor
        'no-new-object': 'error',

        // disallow use of unary operators, ++ and --
        // https://eslint.org/docs/rules/no-plusplus
        'no-plusplus': 'error',

        // disallow certain syntax forms
        // https://eslint.org/docs/rules/no-restricted-syntax
        'no-restricted-syntax': [
            'error',
            {
                selector: 'ForInStatement',
                message: 'for..in loops iterate over the entire prototype chain, which is virtually never what you want. Use Object.{keys,values,entries}, and iterate over the resulting array.',
            },
            {
                selector: 'ForOfStatement',
                message: 'iterators/generators require regenerator-runtime, which is too heavyweight for this guide to allow them. Separately, loops should be avoided in favor of array iterations.',
            },
            {
                selector: 'LabeledStatement',
                message: 'Labels are a form of GOTO; using them makes code confusing and hard to maintain and understand.',
            },
            {
                selector: 'WithStatement',
                message: '`with` is disallowed in strict mode because it makes code impossible to predict and optimize.',
            },
        ],

        // disallow space between function identifier and application
        'no-spaced-func': 'error',

        // disallow tab characters entirely
        'no-tabs': 'error',

        // disallow the use of ternary operators
        'no-ternary': 'off',

        // disallow trailing whitespace at the end of lines
        'no-trailing-spaces': ['error', {
            skipBlankLines: false,
            ignoreComments: false,
        }],

        // disallow dangling underscores in identifiers
        'no-underscore-dangle': ['error', {
            allow: [],
            allowAfterThis: false,
            allowAfterSuper: false,
            enforceInMethodNames: false,
        }],

        // disallow the use of Boolean literals in conditional expressions
        // also, prefer `a || b` over `a ? a : b`
        // https://eslint.org/docs/rules/no-unneeded-ternary
        'no-unneeded-ternary': ['error', { defaultAssignment: false }],

        // disallow whitespace before properties
        // https://eslint.org/docs/rules/no-whitespace-before-property
        'no-whitespace-before-property': 'error',

        // enforce the location of single-line statements
        // https://eslint.org/docs/rules/nonblock-statement-body-position
        'nonblock-statement-body-position': ['error', 'beside', { overrides: {} }],

        // require padding inside curly braces
        'object-curly-spacing': ['error', 'always'],

        // enforce line breaks between braces
        // https://eslint.org/docs/rules/object-curly-newline
        'object-curly-newline': ['error', {
            ObjectExpression: { minProperties: 5, multiline: true, consistent: true },
            ObjectPattern: { minProperties: 5, multiline: true, consistent: true },
            ImportDeclaration: { minProperties: 5, multiline: true, consistent: true },
            ExportDeclaration: { minProperties: 5, multiline: true, consistent: true },
        }],

        // enforce "same line" or "multiple line" on object properties.
        // https://eslint.org/docs/rules/object-property-newline
        'object-property-newline': ['error', {
            allowAllPropertiesOnSameLine: true,
        }],

        // allow just one var statement per function
        'one-var': ['error', 'never'],

        // require a newline around variable declaration
        // https://eslint.org/docs/rules/one-var-declaration-per-line
        'one-var-declaration-per-line': ['error', 'always'],

        // require assignment operator shorthand where possible or prohibit it entirely
        // https://eslint.org/docs/rules/operator-assignment
        'operator-assignment': ['error', 'always'],

        // Requires operator at the beginning of the line in multiline statements
        // https://eslint.org/docs/rules/operator-linebreak
        'operator-linebreak': ['error', 'before', { overrides: { '=': 'none' } }],

        // disallow padding within blocks
        'padded-blocks': ['error', { blocks: 'never', classes: 'never', switches: 'never' }],

        // Require or disallow padding lines between statements
        // https://eslint.org/docs/rules/padding-line-between-statements
        'padding-line-between-statements': 'off',

        // require quotes around object literal property names
        // https://eslint.org/docs/rules/quote-props.html
        'quote-props': ['error', 'as-needed', { keywords: false, unnecessary: true, numbers: false }],

        // specify whether double or single quotes should be used
        quotes: ['error', 'single', { avoidEscape: true }],

        // do not require jsdoc
        // https://eslint.org/docs/rules/require-jsdoc
        'require-jsdoc': 'off',

        // require or disallow use of semicolons instead of ASI
        semi: ['error', 'always'],

        // enforce spacing before and after semicolons
        'semi-spacing': ['error', { before: false, after: true }],

        // Enforce location of semicolons
        // https://eslint.org/docs/rules/semi-style
        'semi-style': ['error', 'last'],

        // requires object keys to be sorted
        'sort-keys': ['off', 'asc', { caseSensitive: false, natural: true }],

        // sort variables within the same declaration block
        'sort-vars': 'off',

        // require or disallow space before blocks
        'space-before-blocks': 'error',

        // require or disallow space before function opening parenthesis
        // https://eslint.org/docs/rules/space-before-function-paren
        'space-before-function-paren': ['error', {
            anonymous: 'always',
            named: 'never',
            asyncArrow: 'always',
        }],

        // require or disallow spaces inside parentheses
        'space-in-parens': ['error', 'never'],

        // require spaces around operators
        'space-infix-ops': 'error',

        // Require or disallow spaces before/after unary operators
        // https://eslint.org/docs/rules/space-unary-ops
        'space-unary-ops': ['error', {
            words: true,
            nonwords: false,
            overrides: {
            },
        }],

        // require or disallow a space immediately following the //or /* in a comment
        // https://eslint.org/docs/rules/spaced-comment
        'spaced-comment': ['error', 'always', {
            line: {
                exceptions: ['-', '+'],
                markers: ['=', '!'], // space here to support sprockets directives
            },
            block: {
                exceptions: ['-', '+'],
                markers: ['=', '!'], // space here to support sprockets directives
                balanced: true,
            },
        }],

        // Enforce spacing around colons of switch statements
        // https://eslint.org/docs/rules/switch-colon-spacing
        'switch-colon-spacing': ['error', { after: true, before: false }],

        // Require or disallow spacing between template tags and their literals
        // https://eslint.org/docs/rules/template-tag-spacing
        'template-tag-spacing': ['error', 'never'],

        // require or disallow the Unicode Byte Order Mark
        // https://eslint.org/docs/rules/unicode-bom
        'unicode-bom': ['error', 'never'],

        // require regex literals to be wrapped in parentheses
        'wrap-regex': 'off',

        // NOTE -------------------------------- variables -------------------------------->>>>>>>>>>>>>

        // enforce or disallow variable initializations at definition
        'init-declarations': 'off',

        // disallow the catch clause parameter name being the same as a variable in the outer scope
        'no-catch-shadow': 'off',

        // disallow deletion of variables
        'no-delete-var': 'error',

        // disallow labels that share a name with a variable
        // https://eslint.org/docs/rules/no-label-var
        'no-label-var': 'error',

        // disallow specific globals
        'no-restricted-globals': [
            'error', 'isFinite', 'isNaN',
            'addEventListener',
            'blur',
            'close',
            'closed',
            'confirm',
            'defaultStatus',
            'event',
            'external',
            'defaultstatus',
            'find',
            'focus',
            'frameElement',
            'frames',
            'history',
            'innerHeight',
            'innerWidth',
            'length',
            'location',
            'locationbar',
            'menubar',
            'moveBy',
            'moveTo',
            'name',
            'onblur',
            'onerror',
            'onfocus',
            'onload',
            'onresize',
            'onunload',
            'open',
            'opener',
            'opera',
            'outerHeight',
            'outerWidth',
            'pageXOffset',
            'pageYOffset',
            'parent',
            'print',
            'removeEventListener',
            'resizeBy',
            'resizeTo',
            'screen',
            'screenLeft',
            'screenTop',
            'screenX',
            'screenY',
            'scroll',
            'scrollbars',
            'scrollBy',
            'scrollTo',
            'scrollX',
            'scrollY',
            'self',
            'status',
            'statusbar',
            'stop',
            'toolbar',
            'top',
        ],

        // disallow declaration of variables already declared in the outer scope
        'no-shadow': 'error',

        // disallow shadowing of names such as arguments
        'no-shadow-restricted-names': 'error',

        // disallow use of undeclared variables unless mentioned in a /*global */ block
        'no-undef': 'error',

        // disallow use of undefined when initializing variables
        'no-undef-init': 'error',

        // disallow use of undefined variable
        // https://eslint.org/docs/rules/no-undefined
        // TODO: enable?
        'no-undefined': 'off',

        // disallow declaration of variables that are not used in the code
        'no-unused-vars': ['error', { vars: 'all', args: 'after-used', ignoreRestSiblings: true }],

        // disallow use of variables before they are defined
        'no-use-before-define': ['error', { functions: true, classes: true, variables: true }],


        // NOTE: ---------------- IMPORTS ------------

        // ensure imports point to files/modules that can be resolved
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-unresolved.md
        'import/no-unresolved': ['error', { commonjs: true, caseSensitive: true }],

        // ensure named imports coupled with named exports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/named.md//when-not-to-use-it
        'import/named': 'error',

        // ensure default import coupled with default export
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/default.md//when-not-to-use-it
        'import/default': 'off',

        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/namespace.md
        'import/namespace': 'off',

        // Helpful warnings:

        // disallow invalid exports, e.g. multiple defaults
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/export.md
        'import/export': 'error',

        // do not allow a default import name to match a named export
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-named-as-default.md
        'import/no-named-as-default': 'error',

        // warn on accessing default export property names that are also named exports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-named-as-default-member.md
        'import/no-named-as-default-member': 'error',

        // disallow use of jsdoc-marked-deprecated imports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-deprecated.md
        'import/no-deprecated': 'off',

        // Forbid the use of extraneous packages
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-extraneous-dependencies.md
        // paths are treated both as absolute paths, and relative to process.cwd()
        'import/no-extraneous-dependencies': ['error', {
            devDependencies: [
                'test/**', // tape, common npm pattern
                'tests/**', // also common npm pattern
                'spec/**', // mocha, rspec-like pattern
                '**/__tests__/**', // jest pattern
                '**/__mocks__/**', // jest pattern
                'test.{js,jsx}', // repos with a single test file
                'test-*.{js,jsx}', // repos with multiple top-level test files
                '**/*{.,_}{test,spec}.{js,jsx}', // tests where the extension or filename suffix denotes that it is a test
                '**/jest.config.js', // jest config
                '**/webpack.config.js', // webpack config
                '**/webpack.config.*.js', // webpack config
                '**/rollup.config.js', // rollup config
                '**/rollup.config.*.js', // rollup config
                '**/gulpfile.js', // gulp config
                '**/gulpfile.*.js', // gulp config
                '**/Gruntfile{,.js}', // grunt config
                '**/protractor.conf.js', // protractor config
                '**/protractor.conf.*.js', // protractor config
            ],
            optionalDependencies: false,
        }],

        // Forbid mutable exports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-mutable-exports.md
        'import/no-mutable-exports': 'error',

        // Module systems:

        // disallow require()
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-commonjs.md
        'import/no-commonjs': 'off',

        // disallow AMD require/define
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-amd.md
        'import/no-amd': 'error',

        // No Node.js builtin modules
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-nodejs-modules.md
        // TODO: enable?
        'import/no-nodejs-modules': 'off',

        // Style guide:

        // disallow non-import statements appearing before import statements
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/first.md
        'import/first': ['error', 'absolute-first'],

        // disallow non-import statements appearing before import statements
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/imports-first.md
        // deprecated: use `import/first`
        'import/imports-first': 'off',

        // disallow duplicate imports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-duplicates.md
        'import/no-duplicates': 'error',

        // disallow namespace imports
        // TODO: enable?
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-namespace.md
        'import/no-namespace': 'off',

        // Ensure consistent use of file extension within the import path
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/extensions.md
        'import/extensions': ['error', 'ignorePackages', {
            js: 'never',
            mjs: 'never',
            jsx: 'never',
        }],

        // Enforce a convention in module import order
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/order.md
        // TODO: enable?
        'import/order': ['off', {
            groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
            'newlines-between': 'never',
        }],

        // Require a newline after the last import/require in a group
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/newline-after-import.md
        'import/newline-after-import': 'error',

        // Require modules with a single export to use a default export
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/prefer-default-export.md
        // "import/prefer-default-export": "error",

        // Restrict which files can be imported in a given folder
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-restricted-paths.md
        'import/no-restricted-paths': 'off',

        // Forbid modules to have too many dependencies
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/max-dependencies.md
        'import/max-dependencies': ['off', { max: 10 }],

        // Forbid import of modules using absolute paths
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-absolute-path.md
        'import/no-absolute-path': 'off',

        // Forbid require() calls with expressions
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-dynamic-require.md
        'import/no-dynamic-require': 'error',

        // prevent importing the submodules of other modules
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-internal-modules.md
        'import/no-internal-modules': ['off', {
            allow: [],
        }],

        // Warn if a module could be mistakenly parsed as a script by a consumer
        // leveraging Unambiguous JavaScript Grammar
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/unambiguous.md
        // this should not be enabled until this proposal has at least been *presented* to TC39.
        // At the moment, it"s not a thing.
        'import/unambiguous': 'off',

        // Forbid Webpack loader syntax in imports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-webpack-loader-syntax.md
        'import/no-webpack-loader-syntax': 'error',

        // Prevent unassigned imports
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-unassigned-import.md
        // importing for side effects is perfectly acceptable, if you need side effects.
        'import/no-unassigned-import': 'off',

        // Prevent importing the default as if it were named
        // https://github.com/benmosher/eslint-plugin-import/blob/master/docs/rules/no-named-default.md
        'import/no-named-default': 'error',

        // Reports if a module"s default export is unnamed
        // https://github.com/benmosher/eslint-plugin-import/blob/d9b712ac7fd1fddc391f7b234827925c160d956f/docs/rules/no-anonymous-default-export.md
        'import/no-anonymous-default-export': ['off', {
            allowArray: false,
            allowArrowFunction: false,
            allowAnonymousClass: false,
            allowAnonymousFunction: false,
            allowLiteral: false,
            allowObject: false,
        }],

        // This rule enforces that all exports are declared at the bottom of the file.
        // https://github.com/benmosher/eslint-plugin-import/blob/98acd6afd04dcb6920b81330114e146dc8532ea4/docs/rules/exports-last.md
        // TODO: enable?
        'import/exports-last': 'off',

        // Reports when named exports are not grouped together in a single export declaration
        // or when multiple assignments to CommonJS module.exports or exports object are present
        // in a single file.
        // https://github.com/benmosher/eslint-plugin-import/blob/44a038c06487964394b1e15b64f3bd34e5d40cde/docs/rules/group-exports.md
        'import/group-exports': 'off',

        // forbid default exports. this is a terrible rule, do not use it.
        // https://github.com/benmosher/eslint-plugin-import/blob/44a038c06487964394b1e15b64f3bd34e5d40cde/docs/rules/no-default-export.md
        'import/no-default-export': 'off',

        // Forbid a module from importing itself
        // https://github.com/benmosher/eslint-plugin-import/blob/44a038c06487964394b1e15b64f3bd34e5d40cde/docs/rules/no-self-import.md
        'import/no-self-import': 'error',

        // Forbid cyclical dependencies between modules
        // https://github.com/benmosher/eslint-plugin-import/blob/d81f48a2506182738409805f5272eff4d77c9348/docs/rules/no-cycle.md
        'import/no-cycle': ['error', { maxDepth: 123456789023456789 }],

        // Ensures that there are no useless path segments
        // https://github.com/benmosher/eslint-plugin-import/issues/1032
        'import/no-useless-path-segments': 'error',

        // NOTE -------------------------------------- errors ----------------------------------------

        // Enforce “for” loop update clause moving the counter in the right direction
        // https://eslint.org/docs/rules/for-direction
        'for-direction': 'error',

        // Enforces that a return statement is present in property getters
        // https://eslint.org/docs/rules/getter-return
        'getter-return': ['error', { allowImplicit: true }],

        // Disallow await inside of loops
        // https://eslint.org/docs/rules/no-await-in-loop
        'no-await-in-loop': 'error',

        // Disallow comparisons to negative zero
        // https://eslint.org/docs/rules/no-compare-neg-zero
        'no-compare-neg-zero': 'error',

        // disallow assignment in conditional expressions
        'no-cond-assign': ['error', 'always'],

        // disallow use of console
        'no-console': 'warn',

        // disallow use of constant expressions in conditions
        'no-constant-condition': 'warn',

        // disallow control characters in regular expressions
        'no-control-regex': 'error',

        // disallow use of debugger
        'no-debugger': 'error',

        // disallow duplicate arguments in functions
        'no-dupe-args': 'error',

        // disallow duplicate keys when creating object literals
        'no-dupe-keys': 'error',

        // disallow a duplicate case label.
        'no-duplicate-case': 'error',

        // disallow empty statements
        'no-empty': 'error',

        // disallow the use of empty character classes in regular expressions
        'no-empty-character-class': 'error',

        // disallow assigning to the exception in a catch block
        'no-ex-assign': 'error',

        // disallow double-negation boolean casts in a boolean context
        // https://eslint.org/docs/rules/no-extra-boolean-cast
        'no-extra-boolean-cast': 'error',

        // disallow unnecessary parentheses
        // https://eslint.org/docs/rules/no-extra-parens
        'no-extra-parens': ['off', 'all', {
            conditionalAssign: true,
            nestedBinaryExpressions: false,
            returnAssign: false,
            ignoreJSX: 'all', // delegate to eslint-plugin-react
            enforceForArrowConditionals: false,
        }],

        // disallow unnecessary semicolons
        'no-extra-semi': 'error',

        // disallow overwriting functions written as function declarations
        'no-func-assign': 'error',

        // disallow function or variable declarations in nested blocks
        'no-inner-declarations': 'error',

        // disallow invalid regular expression strings in the RegExp constructor
        'no-invalid-regexp': 'error',

        // disallow irregular whitespace outside of strings and comments
        'no-irregular-whitespace': 'error',

        // disallow the use of object properties of the global object (Math and JSON) as functions
        'no-obj-calls': 'error',

        // disallow use of Object.prototypes builtins directly
        // https://eslint.org/docs/rules/no-prototype-builtins
        'no-prototype-builtins': 'error',

        // disallow multiple spaces in a regular expression literal
        'no-regex-spaces': 'error',

        // disallow sparse arrays
        'no-sparse-arrays': 'error',

        // Disallow template literal placeholder syntax in regular strings
        // https://eslint.org/docs/rules/no-template-curly-in-string
        'no-template-curly-in-string': 'error',

        // Avoid code that looks like two expressions but is actually one
        // https://eslint.org/docs/rules/no-unexpected-multiline
        'no-unexpected-multiline': 'error',

        // disallow unreachable statements after a return, throw, continue, or break statement
        'no-unreachable': 'error',

        // disallow return/throw/break/continue inside finally blocks
        // https://eslint.org/docs/rules/no-unsafe-finally
        'no-unsafe-finally': 'error',

        // disallow negating the left operand of relational operators
        // https://eslint.org/docs/rules/no-unsafe-negation
        'no-unsafe-negation': 'error',
        // disallow negation of the left operand of an in expression
        // deprecated in favor of no-unsafe-negation
        'no-negated-in-lhs': 'off',

        // disallow comparisons with the value NaN
        'use-isnan': 'error',

        // ensure JSDoc comments are valid
        // https://eslint.org/docs/rules/valid-jsdoc
        'valid-jsdoc': 'off',

        // ensure that the results of typeof are compared against a valid string
        // https://eslint.org/docs/rules/valid-typeof
        'valid-typeof': ['error', { requireStringLiterals: true }],

        // NOTE --------------- REACTJS

        // Specify whether double or single quotes should be used in JSX attributes
        // https://eslint.org/docs/rules/jsx-quotes
        'jsx-quotes': ['error', 'prefer-single'],
        // REVIEW XXX
        'class-methods-use-this': [0, {
            exceptMethods: [
                'render',
                'getInitialState',
                'getDefaultProps',
                'getChildContext',
                'componentWillMount',
                'componentDidMount',
                'componentWillReceiveProps',
                'shouldComponentUpdate',
                'componentWillUpdate',
                'componentDidUpdate',
                'componentWillUnmount',
                'componentDidCatch',
            ],
        }],

        // Prevent missing displayName in a React component definition
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/display-name.md
        'react/display-name': ['off', { ignoreTranspilerName: false }],

        // Forbid certain propTypes (any, array, object)
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/forbid-prop-types.md
        // "react/forbid-prop-types": ["error", {
        //  forbid: ["any", "array", "object"],
        //  checkContextTypes: true,
        //  checkChildContextTypes: true,
        // }],

        // Forbid certain props on DOM Nodes
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/forbid-dom-props.md
        'react/forbid-dom-props': ['off', { forbid: [] }],

        // Enforce boolean attributes notation in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-boolean-value.md
        'react/jsx-boolean-value': ['error', 'never', { always: [] }],

        // Validate closing bracket location in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-closing-bracket-location.md
        'react/jsx-closing-bracket-location': ['error', 'line-aligned'],

        // Validate closing tag location in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-closing-tag-location.md
        'react/jsx-closing-tag-location': 'error',

        // Enforce or disallow spaces inside of curly braces in JSX attributes
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-curly-spacing.md
        'react/jsx-curly-spacing': ['error', 'never', { allowMultiline: true }],

        // Enforce event handler naming conventions in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-handler-names.md
        'react/jsx-handler-names': ['off', {
            eventHandlerPrefix: 'handle',
            eventHandlerPropPrefix: 'on',
        }],

        // Validate props indentation in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-indent-props.md
        'react/jsx-indent-props': ['error', 4],

        // Validate JSX has key prop when in array or iterator
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-key.md
        'react/jsx-key': 'off',

        // Limit maximum of props on a single line in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-max-props-per-line.md
        'react/jsx-max-props-per-line': ['error', { maximum: 1, when: 'multiline' }],

        // Prevent usage of .bind() in JSX props
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-bind.md

        // Prevent duplicate props in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-duplicate-props.md
        'react/jsx-no-duplicate-props': ['error', { ignoreCase: true }],

        // Prevent usage of unwrapped JSX strings
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-literals.md
        'react/jsx-no-literals': ['off', { noStrings: true }],

        // Disallow undeclared variables in JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-undef.md
        'react/jsx-no-undef': 'error',

        // Enforce PascalCase for user-defined JSX components
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-pascal-case.md
        'react/jsx-pascal-case': ['error', {
            allowAllCaps: true,
            ignore: [],
        }],

        // Enforce propTypes declarations alphabetical sorting
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/sort-prop-types.md
        'react/sort-prop-types': ['off', {
            ignoreCase: true,
            callbacksLast: false,
            requiredFirst: false,
            sortShapeProp: true,
        }],

        // Deprecated in favor of react/jsx-sort-props
        'react/jsx-sort-prop-types': 'off',

        // Enforce props alphabetical sorting
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-sort-props.md
        'react/jsx-sort-props': ['off', {
            ignoreCase: true,
            callbacksLast: false,
            shorthandFirst: false,
            shorthandLast: false,
            noSortAlphabetically: false,
            reservedFirst: true,
        }],

        // Enforce defaultProps declarations alphabetical sorting
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/jsx-sort-default-props.md
        'react/jsx-sort-default-props': ['off', {
            ignoreCase: true,
        }],

        // Prevent React to be incorrectly marked as unused
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-uses-react.md
        'react/jsx-uses-react': ['error'],

        // Prevent variables used in JSX to be incorrectly marked as unused
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-uses-vars.md
        'react/jsx-uses-vars': 'error',

        // Prevent usage of dangerous JSX properties
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-danger.md
        'react/no-danger': 'warn',

        // Prevent usage of deprecated methods
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-deprecated.md
        'react/no-deprecated': ['error'],

        // Prevent usage of setState in componentDidMount
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-did-mount-set-state.md
        // this is necessary for server-rendering
        'react/no-did-mount-set-state': 'off',

        // Prevent usage of setState in componentDidUpdate
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-did-update-set-state.md
        'react/no-did-update-set-state': 'error',

        // Prevent usage of setState in componentWillUpdate
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-will-update-set-state.md
        'react/no-will-update-set-state': 'error',

        // Prevent direct mutation of this.state
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-direct-mutation-state.md
        'react/no-direct-mutation-state': 'off',

        // Prevent usage of isMounted
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-is-mounted.md
        'react/no-is-mounted': 'error',

        // Prevent multiple component definition per file
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-multi-comp.md
        'react/no-multi-comp': ['error', { ignoreStateless: true }],

        // Prevent usage of setState
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-set-state.md
        'react/no-set-state': 'off',

        // Prevent using string references
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-string-refs.md
        'react/no-string-refs': 'error',

        // Prevent usage of unknown DOM property
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unknown-property.md
        'react/no-unknown-property': 'error',

        // Require ES6 class declarations over React.createClass
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/prefer-es6-class.md
        'react/prefer-es6-class': ['error', 'always'],

        // Require stateless functions when not using lifecycle methods, setState or ref
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/prefer-stateless-function.md
        'react/prefer-stateless-function': ['error', { ignorePureComponents: true }],

        // Prevent missing props validation in a React component definition
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/prop-types.md
        // NOTE: REVIEW XXX
        // "react/prop-types": ["error", {
        //  ignore: [],
        //  customValidators: [],
        //  skipUndeclared: false
        // }],

        // Prevent missing React when using JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/react-in-jsx-scope.md
        'react/react-in-jsx-scope': 'off',

        // Require render() methods to return something
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/require-render-return.md
        'react/require-render-return': 'error',

        // Prevent extra closing tags for components without children
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/self-closing-comp.md
        'react/self-closing-comp': 'error',

        // Enforce component methods order
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/sort-comp.md
        'react/sort-comp': ['error', {
            order: [
                'static-methods',
                'instance-variables',
                'lifecycle',
                '/^on.+$/',
                'getters',
                'setters',
                '/^(get|set)(?!(InitialState$|DefaultProps$|ChildContext$)).+$/',
                'instance-methods',
                'everything-else',
                'rendering',
            ],
            groups: {
                lifecycle: [
                    'displayName',
                    'propTypes',
                    'contextTypes',
                    'childContextTypes',
                    'mixins',
                    'statics',
                    'defaultProps',
                    'constructor',
                    'getDefaultProps',
                    'getInitialState',
                    'state',
                    'getChildContext',
                    'componentWillMount',
                    'componentDidMount',
                    'componentWillReceiveProps',
                    'shouldComponentUpdate',
                    'componentWillUpdate',
                    'componentDidUpdate',
                    'componentWillUnmount',
                ],
                rendering: [
                    '/^render.+$/',
                    'render',
                ],
            },
        }],

        // Prevent missing parentheses around multilines JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/jsx-wrap-multilines.md
        'react/jsx-wrap-multilines': ['error', {
            declaration: 'parens-new-line',
            assignment: 'parens-new-line',
            return: 'parens-new-line',
            arrow: 'parens-new-line',
            condition: 'parens-new-line',
            logical: 'parens-new-line',
            prop: 'parens-new-line',
        }],

        // Require that the first prop in a JSX element be on a new line when the element is multiline
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-first-prop-new-line.md
        'react/jsx-first-prop-new-line': ['error', 'multiline-multiprop'],

        // Enforce spacing around jsx equals signs
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-equals-spacing.md
        'react/jsx-equals-spacing': ['error', 'never'],

        // Enforce JSX indentation
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-indent.md
        'react/jsx-indent': ['error', 4],

        // Disallow target="_blank" on links
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-target-blank.md
        'react/jsx-no-target-blank': 'error',

        // only .jsx files may have JSX
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-filename-extension.md
        'react/jsx-filename-extension': ['error', { extensions: ['.jsx', '.js'] }],

        // prevent accidental JS comments from being injected into JSX as text
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-no-comment-textnodes.md
        'react/jsx-no-comment-textnodes': 'error',

        // disallow using React.render/ReactDOM.render"s return value
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-render-return-value.md
        'react/no-render-return-value': 'error',

        // require a shouldComponentUpdate method, or PureRenderMixin
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/require-optimization.md
        'react/require-optimization': ['off', { allowDecorators: [] }],

        // warn against using findDOMNode()
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-find-dom-node.md
        'react/no-find-dom-node': 'error',

        // Forbid certain props on Components
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-component-props.md
        'react/forbid-component-props': ['off', { forbid: [] }],

        // Forbid certain elements
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-elements.md
        'react/forbid-elements': ['off', { forbid: [] }],

        // Prevent problem with children and props.dangerouslySetInnerHTML
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-danger-with-children.md
        'react/no-danger-with-children': 'error',

        // Prevent unused propType definitions
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unused-prop-types.md
        'react/no-unused-prop-types': ['error', {
            customValidators: [
            ],
            skipShapeProps: true,
        }],

        // Require style prop value be an object or var
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/style-prop-object.md
        'react/style-prop-object': 'error',

        // Prevent invalid characters from appearing in markup
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unescaped-entities.md
        'react/no-unescaped-entities': 'error',

        // Prevent passing of children as props
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-children-prop.md
        'react/no-children-prop': 'error',

        // Validate whitespace in and around the JSX opening and closing brackets
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/jsx-tag-spacing.md
        'react/jsx-tag-spacing': ['error', {
            closingSlash: 'never',
            beforeSelfClosing: 'always',
            afterOpening: 'never',
            beforeClosing: 'never',
        }],

        // Enforce spaces before the closing bracket of self-closing JSX elements
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-space-before-closing.md
        // Deprecated in favor of jsx-tag-spacing
        'react/jsx-space-before-closing': ['off', 'always'],

        // Prevent usage of Array index in keys
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-array-index-key.md
        'react/no-array-index-key': 'error',

        // Enforce a defaultProps definition for every prop that is not a required prop
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/require-default-props.md
        // NOTE: REVIEW XXX
        // "react/require-default-props": ["error", {
        //  forbidDefaultForRequired: true,
        // }],

        // Forbids using non-exported propTypes
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/forbid-foreign-prop-types.md
        // TODO: enable?
        'react/forbid-foreign-prop-types': ['off', { allowInPropTypes: true }],

        // Prevent void DOM elements from receiving children
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/void-dom-elements-no-children.md
        'react/void-dom-elements-no-children': 'error',

        // Enforce all defaultProps have a corresponding non-required PropType
        // https://github.com/yannickcr/eslint-plugin-react/blob/9e13ae2c51e44872b45cc15bf1ac3a72105bdd0e/docs/rules/default-props-match-prop-types.md
        'react/default-props-match-prop-types': ['error', { allowRequiredDefaults: false }],

        // Prevent usage of shouldComponentUpdate when extending React.PureComponent
        // https://github.com/yannickcr/eslint-plugin-react/blob/9e13ae2c51e44872b45cc15bf1ac3a72105bdd0e/docs/rules/no-redundant-should-component-update.md
        'react/no-redundant-should-component-update': 'error',

        // Prevent unused state values
        // https://github.com/yannickcr/eslint-plugin-react/pull/1103/
        'react/no-unused-state': 'error',

        // Enforces consistent naming for boolean props
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/boolean-prop-naming.md
        'react/boolean-prop-naming': ['off', {
            propTypeNames: ['bool', 'mutuallyExclusiveTrueProps'],
            rule: '^(is|has)[A-Z]([A-Za-z0-9]?)+',
            message: '',
        }],

        // Prevents common casing typos
        // https://github.com/yannickcr/eslint-plugin-react/blob/73abadb697034b5ccb514d79fb4689836fe61f91/docs/rules/no-typos.md
        'react/no-typos': 'error',

        // Enforce curly braces or disallow unnecessary curly braces in JSX props and/or children
        // https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/jsx-curly-brace-presence.md
        'react/jsx-curly-brace-presence': ['error', { props: 'never', children: 'never' }],

        // One JSX Element Per Line
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/jsx-one-expression-per-line.md
        'react/jsx-one-expression-per-line': 0,

        // Enforce consistent usage of destructuring assignment of props, state, and context
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/destructuring-assignment.md
        'react/destructuring-assignment': ['error', 'always'],

        // Prevent using this.state within a this.setState
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/no-access-state-in-setstate.md
        'react/no-access-state-in-setstate': 'error',

        // Prevent usage of button elements without an explicit type attribute
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/button-has-type.md
        'react/button-has-type': ['error', {
            button: true,
            submit: true,
            reset: false,
        }],

        // Ensures inline tags are not rendered without spaces between them
        'react/jsx-child-element-spacing': 'off',

        // Prevent this from being used in stateless functional components
        // https://github.com/yannickcr/eslint-plugin-react/blob/843d71a432baf0f01f598d7cf1eea75ad6896e4b/docs/rules/no-this-in-sfc.md
        'react/no-this-in-sfc': 'error',

        // Validate JSX maximum depth
        // https://github.com/yannickcr/eslint-plugin-react/blob/abe8381c0d6748047224c430ce47f02e40160ed0/docs/rules/jsx-max-depth.md
        'react/jsx-max-depth': 'off',

        // NOTE --------------------------------- REACT-A11Y ---------------------------------------

        // //Enforce that anchors have content
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/anchor-has-content.md
        // "jsx-a11y/anchor-has-content": ["error", { components: [] }],
        //
        // //Require ARIA roles to be valid and non-abstract
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-role.md
        // "jsx-a11y/aria-role": ["error", { ignoreNonDom: false }],
        //
        // //Enforce all aria-* props are valid.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-props.md
        // "jsx-a11y/aria-props": "error",
        //
        // //Enforce ARIA state and property values are valid.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-proptypes.md
        // "jsx-a11y/aria-proptypes": "error",
        //
        // //Enforce that elements that do not support ARIA roles, states, and
        // //properties do not have those attributes.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-unsupported-elements.md
        // "jsx-a11y/aria-unsupported-elements": "error",
        //
        // //Enforce that all elements that require alternative text have meaningful information
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/alt-text.md
        // "jsx-a11y/alt-text": ["error", {
        //  elements: ["img", "object", "area", "input[type='image']"],
        //  img: [],
        //  object: [],
        //  area: [],
        //  "input[type='image']": [],
        // }],
        //
        // //Prevent img alt text from containing redundant words like "image", "picture", or "photo"
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/img-redundant-alt.md
        // "jsx-a11y/img-redundant-alt": "error",
        //
        // //require that JSX labels use "htmlFor"
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/label-has-for.md
        // "jsx-a11y/label-has-for": ["warn", {
        //  components: [],
        //  required: {
        //    every: ["nesting", "id"],
        //  },
        //  allowChildren: false,
        // }],
        //
        // //require that mouseover/out come with focus/blur, for keyboard-only users
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/mouse-events-have-key-events.md
        // "jsx-a11y/mouse-events-have-key-events": "error",
        //
        // //Prevent use of `accessKey`
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-access-key.md
        // "jsx-a11y/no-access-key": "error",
        //
        // //require onBlur instead of onChange
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-onchange.md
        // "jsx-a11y/no-onchange": "off",
        //
        // //Elements with an interactive role and interaction handlers must be focusable
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/interactive-supports-focus.md
        // "jsx-a11y/interactive-supports-focus": "error",
        //
        // //Enforce that elements with ARIA roles must have all required attributes
        // //for that role.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-has-required-aria-props.md
        // "jsx-a11y/role-has-required-aria-props": "error",
        //
        // //Enforce that elements with explicit or implicit roles defined contain
        // //only aria-* properties supported by that role.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-supports-aria-props.md
        // "jsx-a11y/role-supports-aria-props": "error",
        //
        // //Enforce tabIndex value is not greater than zero.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/tabindex-no-positive.md
        // "jsx-a11y/tabindex-no-positive": "error",
        //
        // //ensure <hX> tags have content and are not aria-hidden
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/heading-has-content.md
        // "jsx-a11y/heading-has-content": ["error", { components: [""] }],
        //
        // //require HTML elements to have a "lang" prop
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/html-has-lang.md
        // "jsx-a11y/html-has-lang": "error",
        //
        // //require HTML element"s lang prop to be valid
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/lang.md
        // "jsx-a11y/lang": "error",
        //
        // //prevent distracting elements, like <marquee> and <blink>
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-distracting-elements.md
        // "jsx-a11y/no-distracting-elements": ["error", {
        //  elements: ["marquee", "blink"],
        // }],
        //
        // //only allow <th> to have the "scope" attr
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/scope.md
        // "jsx-a11y/scope": "error",
        //
        // //require onClick be accompanied by onKeyUp/onKeyDown/onKeyPress
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/click-events-have-key-events.md
        // "jsx-a11y/click-events-have-key-events": "warn",
        //
        // //Enforce that DOM elements without semantic behavior not have interaction handlers
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-static-element-interactions.md
        // "jsx-a11y/no-static-element-interactions": ["warn", {
        //  handlers: [
        //    "onClick",
        //    "onMouseDown",
        //    "onMouseUp",
        //    "onKeyPress",
        //    "onKeyDown",
        //    "onKeyUp",
        //  ]
        // }],
        //
        // //A non-interactive element does not support event handlers (mouse and key handlers)
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-noninteractive-element-interactions.md
        // "jsx-a11y/no-noninteractive-element-interactions": ["warn", {
        //  handlers: [
        //    "onClick",
        //    "onMouseDown",
        //    "onMouseUp",
        //    "onKeyPress",
        //    "onKeyDown",
        //    "onKeyUp",
        //  ]
        // }],
        //
        // //ensure emoji are accessible
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/accessible-emoji.md
        // "jsx-a11y/accessible-emoji": "warn",
        //
        // //elements with aria-activedescendant must be tabbable
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-activedescendant-has-tabindex.md
        // "jsx-a11y/aria-activedescendant-has-tabindex": "warn",
        //
        // //ensure iframe elements have a unique title
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/iframe-has-title.md
        // "jsx-a11y/iframe-has-title": "warn",
        //
        // //prohibit autoFocus prop
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-autofocus.md
        // "jsx-a11y/no-autofocus": ["warn", { ignoreNonDOM: true }],
        //
        // //ensure HTML elements do not specify redundant ARIA roles
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-redundant-roles.md
        // "jsx-a11y/no-redundant-roles": "warn",
        //
        // //media elements must have captions
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/media-has-caption.md
        // "jsx-a11y/media-has-caption": ["warn", {
        //  audio: [],
        //  video: [],
        //  track: [],
        // }],
        //
        // //WAI-ARIA roles should not be used to convert an interactive element to non-interactive
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-interactive-element-to-noninteractive-role.md
        // "jsx-a11y/no-interactive-element-to-noninteractive-role": ["warn", {
        //  tr: ["none", "presentation"],
        // }],
        //
        // //WAI-ARIA roles should not be used to convert a non-interactive element to interactive
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-noninteractive-element-to-interactive-role.md
        // "jsx-a11y/no-noninteractive-element-to-interactive-role": ["warn", {
        //  ul: ["listbox", "menu", "menubar", "radiogroup", "tablist", "tree", "treegrid"],
        //  ol: ["listbox", "menu", "menubar", "radiogroup", "tablist", "tree", "treegrid"],
        //  li: ["menuitem", "option", "row", "tab", "treeitem"],
        //  table: ["grid"],
        //  td: ["gridcell"],
        // }],
        //
        // //Tab key navigation should be limited to elements on the page that can be interacted with.
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-noninteractive-tabindex.md
        // "jsx-a11y/no-noninteractive-tabindex": ["warn", {
        //  tags: [],
        //  roles: ["tabpanel"],
        // }],
        //
        // //ensure <a> tags are valid
        // //https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/0745af376cdc8686d85a361ce36952b1fb1ccf6e/docs/rules/anchor-is-valid.md
        // "jsx-a11y/anchor-is-valid": ["warn", {
        //  components: ["Link"],
        //  specialLink: ["to"],
        //  aspects: ["noHref", "invalidHref", "preferButton"],
        // }],

        // NOTE ------------------------------------ test ------------------------------------------

        'jest/no-disabled-tests': 'warn',
        'jest/no-focused-tests': 'error',
        'jest/no-identical-title': 'error',
        'jest/prefer-to-have-length': 'warn',
        'jest/valid-expect': 'error',

        // ------------------------------------------ RULES END -------------------------------------------------
    },
};
