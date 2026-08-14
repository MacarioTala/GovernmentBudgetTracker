from etl.datamodel import GAOFunction


import streamlit as st
from bs4 import BeautifulSoup


@st.cache_data
def get_GAO_functions()->list[GAOFunction]:
    """ This function parses the GAO glossary expecting the following format:
    SuperCode
    SuperFunction
    SuperDescription
        Subcode 1
        Subfunction 1
        Subdescription 1
        Subcode n
        Subfunction n
        Subdescription n
    SuperCode 2
    ...
    Source: GAO
    """
    with open("GAO.html","r", encoding="utf-8") as f:
        soup = BeautifulSoup(f,"html.parser")
    gao_text = soup.get_text("\n",strip=True)

    start_marker = "Code: 050;"
    end_marker = "Source: GAO."

    start_index = gao_text.find(start_marker)
    end_index = gao_text.find(end_marker)

    if start_index==-1 or end_index==-1:
        raise ValueError("Cannot locate definitions section")

    important_bits = gao_text[start_index:end_index]

    lines = important_bits.splitlines()

    supercode_marker = "Code:"
    subcode_marker = "Subcode:"
    function_marker = "Function:"
    subfunction_marker="Subfunction:"

    GAOFunctions=[]

    #Superfunction state
    current_supercode=None
    current_function=None
    current_superfunction_description=[]
    current_subcodes=[]

    #Subfunction state
    current_subcode=None
    current_subfunction=None
    current_subfunction_description=[]

    #When we hit a subcode, the description lines belong to the subcode
    subcode_marker_hit = False

    for line in lines:

        #New Superfunction
        if supercode_marker in line:
            #If the previous superfunction had a final subfunction, the subfunction is now saved
            if current_subcode:
                            GAOFunctions.append(
                                GAOFunction(
                                    code=current_subcode,
                                    name=current_subfunction,
                                    description="\n".join(current_subfunction_description).strip(),
                                    supercode=current_supercode
                                )
                            )
            #The superfunction we're building is now also finished
            if current_supercode:
                GAOFunctions.append(
                    GAOFunction(
                        code=current_supercode,
                        name=current_function,
                        description="\n".join(current_superfunction_description).strip(),
                        subcodes=current_subcodes.copy()))

            #start a new superfunction
            current_supercode = line.removeprefix(supercode_marker).strip().removesuffix(";")
            current_function = None
            current_superfunction_description = []
            current_subcodes = []

            #clear subcode state, because there's a new superfunction
            current_subcode = None
            current_subfunction = None
            current_subfunction_description=[]
            subcode_marker_hit = False

        #Superfunction name
        elif function_marker in line:
            current_function = line.removeprefix(function_marker).strip().removesuffix(".")

        #new Subfunction
        elif subcode_marker in line:
            #if previous subfunction exists, save it now
            if current_subcode:
                GAOFunctions.append(
                    GAOFunction(
                        code=current_subcode,
                        name=current_subfunction,
                        description="\n".join(current_subfunction_description).strip(),
                        supercode=current_supercode
                    )
                )
            #start new subfunction
            current_subcode= line.removeprefix(subcode_marker).strip().removesuffix(";")
            current_subfunction=None
            current_subfunction_description=[]

            subcode_marker_hit = True
            current_subcodes.append(current_subcode)

        elif subfunction_marker in line:
            current_subfunction= line.removeprefix(subfunction_marker).strip().removesuffix(".")

        else:
            if not subcode_marker_hit:
                current_superfunction_description.append(line)
            else:
                current_subfunction_description.append(line)

    #save last subfunction of last superfunction
    if current_subcode:
        GAOFunctions.append(
            GAOFunction(
                code=current_subcode,
                name=current_subfunction,
                description="\n".join(current_subfunction_description).strip(),
                supercode=current_supercode
            )
        )

    #save last superfunction
    if current_supercode:
        GAOFunctions.append(
            GAOFunction(
                code=current_supercode,
                name=current_function,
                description="\n".join(current_superfunction_description).strip(),
                subcodes=current_subcodes.copy()))

    return GAOFunctions