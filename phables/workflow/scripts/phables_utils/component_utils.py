def get_components(
    assembly_graph,
    unitig_names,
    smg_unitigs,
    unitig_phrogs,
    circular,
    edges_lengths,
    cicular_len,
    phrog_dict
):
    """
    Get connected components with PHROGs and no SMGs.
    """

    pruned_vs = {}

    i = 0

    comp_phrogs = {}
    phrogs_found = set()

    for component in assembly_graph.components():

        head_present = False
        connector_present = False
        tail_present = False
        lysis_present = False

        if len(component) > 1:

            for unitig in component:

                if unitig_names[unitig] in smg_unitigs:
                    break
                elif unitig_names[unitig] in unitig_phrogs:

                    for phrog in unitig_phrogs[unitig_names[unitig]]:
                        if "head and packaging" in phrog_dict[phrog]:
                            head_present = True
                        if "connector" in phrog_dict[phrog]:
                            connector_present = True
                        if "portal" in phrog_dict[phrog]:
                            tail_present = True
                        if "lysis" in phrog_dict[phrog]:
                            lysis_present = True
                        
                        phrogs_found.add(phrog)

            if (head_present or connector_present or tail_present or lysis_present):
                pruned_vs[i] = component
                comp_phrogs[i] = phrogs_found
                i += 1

        if len(component) == 1:

            unitig = component[0]
            phrogs_present = False

            for phrog in unitig_phrogs[unitig_names[unitig]]:
                if "head and packaging" in phrog_dict[phrog]:
                    head_present = True
                if "connector" in phrog_dict[phrog]:
                    connector_present = True
                if "portal" in phrog_dict[phrog]:
                    tail_present = True
                if "lysis" in phrog_dict[phrog]:
                    lysis_present = True
                
                phrogs_found.add(phrog)

            if (head_present or connector_present or tail_present or lysis_present):
                phrogs_present = True

            if (
                phrogs_present
                and unitig_names[unitig] in circular
                and edges_lengths[unitig_names[unitig]] > cicular_len
            ):
                pruned_vs[i] = component
                comp_phrogs[i] = phrogs_found
                i += 1

    return pruned_vs, comp_phrogs
