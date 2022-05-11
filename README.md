## THE FUSION CONFIGURATOR

This is the Fusion Configurator. My first React App and first time using JavaScript, so inevitably some things are done slightly inneficiently (edit 11/05/2022 - horribly). But it runs fine and works.

Link: https://www.fusionconfigurator.com/

### How it all ties together

Basically we've got 'App.js' which sends data down to sub components and sub components of sub components etc etc. Therefore it's quite a large file, holds a fair few variables and does most of the actual data processing. 

The configuration of the website/websites: config files, prices, languages etc is done using a DJango, python backend as it was quick and easy to implement.

### Dependencies

All the packages it use are under the MIT license, the list of which can be seen below. I only introduced dependencies where I really had to, and it made sense to outsource code. For example, for creating PDFs and XLSX files.

1. React-Bootstrap - https://react-bootstrap.github.io/
2. Html2Canvas - https://html2canvas.hertzen.com/
3. React-PDF - https://react-pdf.org/
4. React-device-detect - https://www.npmjs.com/package/react-device-detect
5. React-Modal - https://github.com/reactjs/react-modal
6. React-data-export - https://www.npmjs.com/package/react-data-export
7. File-saver - https://www.npmjs.com/package/file-saver


