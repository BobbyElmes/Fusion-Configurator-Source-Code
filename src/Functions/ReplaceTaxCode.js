function replaceTaxCode(source, code, language) {
    if (code != null && code != "") {
        return source.replace("[TAX]", code);
    }
    else {
        switch (language) {
            case 1:
                return source.replace("[TAX]", "BTW");
            case 2:
                return source.replace("[TAX]", "MwSt");
            case 3:
                return source.replace("[TAX]", "MVA");
            default:
                return source.replace("[TAX]", "VAT");
        }
    }
}

export default replaceTaxCode;