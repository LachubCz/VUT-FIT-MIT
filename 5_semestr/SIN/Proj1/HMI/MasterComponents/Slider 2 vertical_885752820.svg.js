

//this function is called on view loaded
//you can put all your initialization code here
//parameter svg is the SVG Document
//parameter component is the Component element
//parameter properties are the componens' properties
//parameter values are filled in values in properties for type object
 function Compprefix_id__init(svg,component,properties,values){
     var tag=properties.list[0].value;
    
    var callback=properties.list[5].value;
    var log=properties.list[6].value;
    var round=parseInt(properties.list[4].value);
    
    if (callback || log)
    {
        $(component).mouseup(function(){
            debugger;
          
            var value=0;
            var children=component.childNodes
            for (var i=0;i<children.length;i++)
            {
                if (children[i].__aktValue)
                {
                var value=children[i].__aktValue
                break;
                }
                var ch=children[i].childNodes
                for (var j=0;j<ch.length;j++)
                {
                   if (ch[j].__aktValue)
                    {
                    var value=ch[j].__aktValue
                    break;
                    } 
                }
            }
            
            var valuefix=(value).toFixed(round);
            if (callback)
            {
                myscada[callback](valuefix);
            }
            if (log)
            {
                var log2=myscada.replaceValueForHash(log,valuefix);
                myscada.logUserAction(log2,0);
            }
           
        });
    }
    
    //
 }

 //This funcion is called each time
 //new data are avaiable
 function Compprefix_id__animate(data){


 }

