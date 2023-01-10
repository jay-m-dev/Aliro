/* ~This file is part of the Aliro library~

Copyright (C) 2017 Epistasis Lab, University of Pennsylvania

Aliro is maintained by:
    - Heather Williams (hwilli@upenn.edu)
    - Weixuan Fu (weixuanf@upenn.edu)
    - William La Cava (lacava@upenn.edu)
    - Michael Stauffer (stauffer@upenn.edu)
    - and many other generous open source contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

(Autogenerated header, do not modify)

*/
import React from 'react';
import { Header, Button, Popup, Checkbox, Divider, Grid} from 'semantic-ui-react';
import { Link } from 'react-router';

function SceneHeader({
  header,
  subheader,
  btnText,
  btnIcon,
  linkText
}) {






  var [eventsEnabled, setEventsEnabled] = React.useState(true)
  var [open, setOpen] = React.useState(true)


  function clearFileIcons(currentFile) {
    
    
    // var selectedFileIconds=document.getElementById(currentFile)
    // selectedFileIconds.parentNode.removeChild(selectedFileIconds);

    // parse currentFile to get the number
    var currentFileNumber = currentFile.split("_")[2];
    

    var fileIcon = document.getElementById("preloaded_data_" + currentFileNumber);
    if (fileIcon) {
      fileIcon.parentNode.removeChild(fileIcon); 
    }

  }
  
  if (window.location.href.includes("upload_") == false) {
    clearFileIcons("preloaded_data_1");
    clearFileIcons("preloaded_data_2");
    clearFileIcons("preloaded_data_3");
    clearFileIcons("preloaded_data_4");
    clearFileIcons("preloaded_data_5");
  

  }



  // document.getElementById("aiTooglePopup").style.cssText += ';display:none !important;';




  return (
    <div className="scene-header">
      <Header
        inverted
        size="huge"
        content={header}
        subheader={subheader}
      />

      {/* <Grid.Column>
        <Checkbox
          // make it unvisible 
          style={{display: 'none'}}
          checked={open}
          label={{ children: <code>open</code> }}
          onChange={(e, data) => setOpen(data.checked)}
        />
        <Divider fitted hidden />
        <Checkbox
        style={{display: 'none'}}
          checked={eventsEnabled}
          label={{ children: <code>eventsEnabled</code> }}
          onChange={(e, data) => setEventsEnabled(data.checked)}
        />
      </Grid.Column> */}

      {/* {btnText &&
        <Button
          inverted
          color="blue"
          compact
          size="small"
          icon={btnIcon}
          content={btnText}
          as={ Link }
          to={linkText}
        />
      } */}
      {btnText &&
      <Popup
        id = "addNewPopup_former"
        // this below button in trigger is the blue button for adding new data.
        // for now it is removed.

        // trigger=
        // {<Button
        //   inverted
        //   color="blue"
        //   compact
        //   size="small"
        //   icon={btnIcon}
        //   content={btnText}
        //   as={ Link }
        //   to={linkText}
        // />}
       
        content='Step 1: click this button to upload your dataset.'

        position='right center'

        
 

        
        open = {false}

        

        
      />

      }

      
    </div>
  );
}

export default SceneHeader;
