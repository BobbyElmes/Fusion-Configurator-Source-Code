import React from 'react';
import './Cell.css'
import Button from 'react-bootstrap/Button';

//display an individual kit item,
//which consists of an uninteractable button, a product ID and a quantity
class KitItem extends React.Component {
    constructor(props) {
        super(props)

    }

    decideItem(item) {
        //switch the item to see what css is needed for the button
        var color = ""
        switch (item) {
            case "F16-TC":
            case "F16-LC":
                color = "TC"
                break;
            case "F16-TR":
            case "F16-LR":
                color = "TR"
                break;
            case "F16-TL":
            case "F16-LL":
                color = "TL"
                break;
            case "F16-T-LR":
                color = "T-LR"
                break;
            case "F16-TY":
            case "F16-LY":
                color = "TY"
                break;
            case "F16-J":
            case "F16-LJ":
                color = "J"
                break;
            case "VAT-16":
            case "VAL-16":
                color = "VAT-16"
                break;
            case "F16-VC":
            case "F16-VB":
                color ="WindowAlternate"
                break;
            case "F16-CLT":
            case "F16-LCLT":
                color = "CLT";
                break;
            case "F16-CRT":
            case "F16-LCRT":
                color = "CRT";
                break;
            case "F16-CRB":
            case "F16-LCRB":
                color = "CRB";
                break;
            case "F16-CLB":
            case "F16-LCLB":
                color = "CLB";
                break;
            case "F16-CLB-S":
            case "F16-LCLB-S":
                color = "CLB-S";
                break;
        }
        return color
    }

    //render the button, with text to its right
    render() {
        var color = this.decideItem(this.props.item[0])
        var cell
        if (color != "") {
            if (color == "Window") {
                cell = <button style={{ marginRight: "10px", cursor: "context-menu", width: "25px", height: "25px" }} className={"WindowAlternate" + ' shadow-none'}> </button>
                
            }
            else
                cell = <button style={{ marginRight: "10px", cursor: "context-menu", width: "25px", height: "25px" }} className={color + ' shadow-none'}> </button>
        }

        var comingSoon = "";
        if (false) {
            if (!this.props.mobile)
                comingSoon = <div>&#9888; {this.props.words[25][this.props.language]}</div>;
            else
                comingSoon = <div style={{ marginLeft: "15px" }}>&#9888;</div>
        }
        
        if(!this.props.mobile)
            return (<div style={{ display: "flex", flexDirection: "row", marginBottom: "-10px", minWidth: "130px" }} >
                        {cell}
                        <p style={{ fontFamily: "arial" }}>{this.props.id}</p>
                        <div style={{ position: "absolute", marginLeft: "130px" }}>
                            <div style={{ display: "flex", flexDirection: "row"}}>
                        <p style={{ fontFamily: "arial", marginLeft: "30px" }}>{Math.ceil(this.props.item[1])}</p>
                        <p style={{ fontFamily: "arial", marginLeft: "20px", fontSize: "15px", color: "red"}}>{comingSoon}</p>
                            </div>
                        </div>
            </div>)
        else
            return (<div style={{ display: "flex", flexDirection: "row", marginBottom: "-10px", minWidth: "130px" }} >
                {cell}
                <p style={{ fontFamily: "arial" }}>{this.props.id}</p>
                <div style={{ position: "absolute", marginLeft: "150px" }}>
                    <div style={{ display: "flex", flexDirection: "row" }}>
                        <p style={{ fontFamily: "arial" }}>{Math.ceil(this.props.item[1])}</p>
                        <p style={{ fontFamily: "arial", fontSize: "15px", color: "red" }}>{comingSoon}</p>
                    </div>
                    
                </div>
                
            </div>)
    }
}


export default KitItem;