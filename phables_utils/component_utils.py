def get_components(
    assembly_graph,
    contig_names,
    smg_contigs,
    contig_phrogs,
    circular,
    edges_lengths,
    cicular_len,
):
    """
    Get connected components with PHROGs and no SMGs.
    """

    pruned_vs = {}

    i = 0

    for component in assembly_graph.components():

        if len(component) > 1:

            has_phrog = False

            for contig in component:

                if contig_names[contig] in smg_contigs:
                    break
                elif contig_names[contig] in contig_phrogs:
                    if (
                        "terminase large subunit head and packaging"
                        in contig_phrogs[contig_names[contig]]
                        or "capsid assembly protein tail"
                        in contig_phrogs[contig_names[contig]]
                        or "portal protein head and packaging"
                        in contig_phrogs[contig_names[contig]]
                    ):
                        has_phrog = True

            if has_phrog:
                pruned_vs[i] = component
                i += 1

        if len(component) == 1:

            if (
                contig_names[component[0]] in contig_phrogs
                and contig_names[component[0]] in circular
                and edges_lengths[contig_names[component[0]]] > cicular_len
            ):
                pruned_vs[i] = component
                i += 1

    return pruned_vs
